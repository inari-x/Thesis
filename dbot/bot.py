import os
import asyncio
import discord
from discord.ext import commands 
import llm_completions
import requests

REQUEST_QUEUE_COMPLETION =	asyncio.Queue()
RESPONSE_QUEUE_COMPLETION = asyncio. Queue()
REQUEST_QUEUE_TRANSLATION = asyncio.Queue()
RESPONSE_QUEUE_TRANSLATION = asyncio.Queue()
REQUEST_QUEUE_ENHANCEMENT = asyncio.Queue()
RESPONSE_QUEUE_ENHANCEMENT = asyncio.Queue()


# fix later - https://pypi.org/project/hotreload/

import context_handler
from request_queue import init_request_queue, llm_complete_request
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
SYSTEM_MESSAGE = "You are an AI assistant" #bot persona

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix=".", intents=intents)

llama2_url = "http://127.0.0.1:8000/v1/completions/"


async def translate_text(prompt, source_language, target_language):
    payload = {
        "prompt": f"\n\n### Translate the following from {source_language} to {target_language}:\n{prompt}\n\n### Response:\n",
            "stop": [
                "\n",
                "###"
            ],
            "max_tokens": 500,
    }

    try:
        await REQUEST_QUEUE_TRANSLATION.put((prompt, source_language, target_language))
        print(f"Translation request: {prompt} from {source_language} to {target_language}")
        response = requests.post(llama2_url, json=payload)
        print(f"Translation size of queue: {REQUEST_QUEUE_TRANSLATION.qsize()}")

        if response.status_code == 200:
            translated_text = response.json().get("choices")[0].get("text")
            RESPONSE_QUEUE_TRANSLATION = response.json()
            print(f"Translation response: {RESPONSE_QUEUE_TRANSLATION}")
            return translated_text
        else:
            return "Sorry, there was an error with the translation."

    except Exception as e:
        return str(e)
    
async def complete_text(prompt): 
    payload = {
        "prompt": f"\n\n### Complete the following:\n{prompt}\n\n### Response:\n",
            "stop": [
                "\n",
                "###"
            ],
            "max_tokens": 500,
    }

    try:
        REQUEST_QUEUE_COMPLETION.put(prompt)
        print(f"Completion request: {prompt}")
        response = requests.post(llama2_url, json=payload)

        if response.status_code == 200:
            completed_text = response.json().get("choices")[0].get("text")
            RESPONSE_QUEUE_COMPLETION = response.json()
            print(f"Completion response: {RESPONSE_QUEUE_COMPLETION}")
            return completed_text
        else:
            return "Sorry, there was an error with the completion."
        
    except Exception as e:
        return str(e)

    

def enhance_text(prompt):
    payload = {
        "prompt": f"\n\n### Enhance the following:\n{prompt}\n\n### Response:\n",
            "stop": [
                "\n",
                "###"
            ], 
            "max_tokens": 500,
    }

    try:
        REQUEST_QUEUE_ENHANCEMENT.put(prompt)
        print(f"Enhancement request: {prompt}")
        response = requests.post(llama2_url, json=payload)


        if response.status_code == 200:
            enhanced_text = response.json().get("choices")[0].get("text")
            RESPONSE_QUEUE_ENHANCEMENT = response.json()
            print(f"Enhancement response: {RESPONSE_QUEUE_ENHANCEMENT}")
            return enhanced_text
        else:
            return "Sorry, there was an error with the enhancement."
        
    except Exception as e:
        return str(e)
    
    
@client.event
async def on_ready():
    print("Bot is ready")
    print("Completion:", REQUEST_QUEUE_COMPLETION.qsize())
    print("Translation:", REQUEST_QUEUE_TRANSLATION.qsize())
    print("Enhancement:", REQUEST_QUEUE_ENHANCEMENT.qsize())

class HelpButtons(discord.ui.View):
    def __init__(self):
        super().__init__()
    
    @discord.ui.button(label="Translate", style=discord.ButtonStyle.green)
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(content="Please provide the text to translate formatted as '<source language> <target language> <message>'\nEx: german english how are you.")
        try:
            response = await client.wait_for(
                "message",
                check=lambda m: m.author == interaction.user and m.channel == interaction.channel,
                timeout=60.0  # Adjust the timeout as needed
            )
        except asyncio.TimeoutError:
            await interaction.followup.send("Translation request timed out.")
            return

        text_to_translate = response.content
        print(f"Received message: {text_to_translate} from {response.author}")

        source_language = text_to_translate.split(" ")[0]
        target_language = text_to_translate.split(" ")[1]
        text_to_translate = " ".join(text_to_translate.split(" ")[2:])

        # Call the translate_text function to get the translation
        translated_text = await translate_text(text_to_translate, source_language, target_language)

        # Send the translated text as a response
        await interaction.followup.send(f"Translation:\n {translated_text}", view=HelpButtons())


    @discord.ui.button(label="Complete", style=discord.ButtonStyle.red)
    async def button2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(content="Please provide the text to complete.")
        try:
            response = await client.wait_for(
                "message",
                check=lambda m: m.author == interaction.user and m.channel == interaction.channel,
                timeout=60.0  # Adjust the timeout as needed
            )
        except asyncio.TimeoutError:
            await interaction.followup.send("Completion request timed out.")
            return
        
        text_to_complete = response.content
        print(f"Received message: {text_to_complete} from {response.author}")

        # Call the complete_text function to get the completion
        completed_text = await complete_text(text_to_complete)

        # Send the completed text as a response
        await interaction.followup.send(f"Completion:\n {completed_text}", view=HelpButtons())


    @discord.ui.button(label="Enhance", style=discord.ButtonStyle.blurple)
    async def button3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(content="Please provide the text to enhance.")
        try:
            response = await client.wait_for(
                "message",
                check=lambda m: m.author == interaction.user and m.channel == interaction.channel,
                timeout=60.0  # Adjust the timeout as needed
            )
        except asyncio.TimeoutError:
            await interaction.followup.send("Enhancement request timed out.")
            return
        
        text_to_enhance = response.content
        print(f"Received message: {text_to_enhance} from {response.author}")

        # Call the enhance_text function to get the enhancement
        enhanced_text = await enhance_text(text_to_enhance)

        # Send the enhanced text as a response
        await interaction.followup.send(f"Enhancement:\n {enhanced_text}", view=HelpButtons())

            
        
@client.command()
async def button(ctx):
    message = await ctx.send("Welcome to the bot!", view=HelpButtons())
    ctx.view.message = message

@client.event
async def on_message(message):
    is_dm = isinstance(message.channel, discord.channel.DMChannel)
    context_id = str(message.channel)
    if is_dm:
        context_id = str(message.author.id)

    if message.author == client.user:

        return
    
    if message.content.startswith("!reset"):
        reset_result = context_handler.reset_context(context_id)
        print(f"Reset result: {reset_result}")
        await message.reply(reset_result, mention_author=True)
        return
    
    if discord.ui.Button.label == "Translate":
        print("Translate button pressed")
        # Extract and enqueue translation request
        text_to_translate = message.content[len("translate"):].strip()
        await REQUEST_QUEUE_TRANSLATION.put((text_to_translate, context_id))
        return

    if discord.ui.Button.label == "Complete":
        # Extract and enqueue completion request
        text_to_complete = message.content[len("complete"):].strip()
        await REQUEST_QUEUE_COMPLETION.put((text_to_complete, context_id))
        return

    if discord.ui.Button.label == "Enhance":
        # Extract and enqueue enhancement request
        text_to_enhance = message.content[len("enhance"):].strip()
        await REQUEST_QUEUE_ENHANCEMENT.put((text_to_enhance, context_id))
        return
    
    await client.process_commands(message)
    
client.run(TOKEN) 

