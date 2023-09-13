import os
import asyncio
import discord
from discord.ext import commands 
import requests

# fix later - https://pypi.org/project/hotreload/
# import time
# import logging
# from hotreload import Loader

import context_handler
from request_queue import init_request_queue, llm_complete_request
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix=".", intents=intents)

llama2_url = "http://127.0.0.1:8000/v1/completions/"

def translate_text(prompt, source_language, target_language):
    payload = {
        "prompt": f"\n\n### Translate the following from {source_language} to {target_language}:\n{prompt}\n\n### Response:\n",
            "stop": [
                "\n",
                "###"
            ]
    }

    try:
        response = requests.post(llama2_url, json=payload)

        if response.status_code == 200:
            translated_text = response.json().get("choices")[0].get("text")
            return translated_text
        else:
            return "Sorry, there was an error with the translation."

    except Exception as e:
        return str(e)
    
def complete_text(prompt): 
    payload = {
        "prompt": f"\n\n### Complete the following:\n{prompt}\n\n### Response:\n",
            "stop": [
                "\n",
                "###"
            ]
    }

    try:
        response = requests.post(llama2_url, json=payload)

        if response.status_code == 200:
            completed_text = response.json().get("choices")[0].get("text")
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
            ]
    }

    try:
        response = requests.post(llama2_url, json=payload)

        if response.status_code == 200:
            enhanced_text = response.json().get("choices")[0].get("text")
            return enhanced_text
        else:
            return "Sorry, there was an error with the enhancement."
        
    except Exception as e:
        return str(e)
    

    

class HelpButtons(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Translate", style=discord.ButtonStyle.green)
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(content="Please provide the text to translate formatted as '<source language> <target language> <message>'\nEx: german english how are you?")
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
        translated_text = translate_text(text_to_translate, source_language, target_language)

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
        completed_text = complete_text(text_to_complete)

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
        enhanced_text = enhance_text(text_to_enhance)

        # Send the enhanced text as a response
        await interaction.followup.send(f"Enhancement:\n {enhanced_text}", view=HelpButtons())

        
# @client.event
# async def on_ready():
#     await init_request_queue()
#     print(f'logged in as {client.user}')

# @client.event
# async def on_message(message):
#     is_dm = isinstance(message.channel, discord.channel.DMChannel)
#     at_mention = f'<@{client.user.id}>'
#     context_id = str(message.channel)
#     if is_dm:
#         context_id = str(message.author.id)
#     # we do not want the bot to reply to itself
#     if message.author.id == client.user.id:
#         return

#     # If message is DM or @sandbox
#     if is_dm or message.content.startswith(at_mention):
#         # console log here
#         print(f"Received message: {message.content} from {message.author}")
#         stripped_message = str(message.content).replace(at_mention, '').strip()
#         if stripped_message.startswith("!reset"):
#             reset_result = context_handler.reset_context(context_id)
#             await message.reply(reset_result, mention_author=True)
#             return
#         if stripped_message.startswith("!complete"):
#             complete_response = await llm_complete_request(stripped_message, context_id, complete_only=True)
#             await message.reply(complete_response, mention_author=True)
#             return
#         complete_response = await llm_complete_request(stripped_message, context_id, complete_only=False)
#         await message.reply(complete_response, mention_author=True)
            
        
@client.command()
async def button(ctx):
    message = await ctx.send("Welcome to the bot!", view=HelpButtons())
    ctx.view.message = message

@client.event
async def on_message(message):
    if message.author == client.user:
        return
 
    await client.process_commands(message)
    
client.run(TOKEN) 

