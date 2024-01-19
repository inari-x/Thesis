#------------------------------------------------------------------------------
# # Section 1: Imported Libraries and Modules
#------------------------------------------------------------------------------

# Explanation: The script begins by importing necessary libraries and modules, 
# including those for handling Discord interactions, making HTTP requests, and 
# managing configurations.

import os
import asyncio
import aiohttp
import discord
import config_handler
import context_handler
from discord.ext import commands 
from discord import ui, app_commands
from dotenv import load_dotenv
from config_modal import ConfigBotAIsettings

#------------------------------------------------------------------------------
# # Section 2: Global Variables
#------------------------------------------------------------------------------

# Explanation: Global variables are declared to manage user context data.
USER_CONTEXT = {}

#------------------------------------------------------------------------------
# Section 3: Token and Intent Configuration
#------------------------------------------------------------------------------

# Explanation: Global variables are declared to manage various queues for 
# different request types and user context data.

load_dotenv()
TOKEN = os.getenv("TOKEN")
SYSTEM_MESSAGE = "You are an AI assistant" #bot persona
APPLICATION_ID = os.getenv("APPLICATION_ID")

intents = discord.Intents.default() 
intents.message_content = True


#------------------------------------------------------------------------------
# Section 4: Client Class
#------------------------------------------------------------------------------

# Explanation: A custom client class, "MyClient," is defined to handle bot 
# interactions and sync application commands.

class MyClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents, application_id = APPLICATION_ID)
        self.tree = app_commands.CommandTree(self)

async def setup_hook(self):
    await self.tree.sync()

client = commands.Bot(command_prefix=".", intents=intents)

############################ LLAMA2 API ENDPOINT ##############################
# Explanation: The HTTP server running through 
# python-llama-cpp[server] is the API between the Python 
# chatbot and the language model. This is accessed through 
# 127.0.0.1, on port 8000, by default.

llama2_url = "http://127.0.0.1:8000/v1/completions/"

############################ T R A N S L A T I O N ############################

async def translate_text(prompt, source_language, target_language, user_id):
    config = config_handler.get_config(user_id)
    context = context_handler.load_context(user_id)
    prompt = prompt.replace("\n", " ") 
    payload = {
        "prompt": f"\n\n### Translate the following from {source_language} to {target_language}:\n{prompt}\n\n### Response:\n",
            "stop": [
                "\n",
                "###"
            ],
            "max_tokens": config["max_tokens"],
    }
    try:
        #aiohttp.ClientSession() is used as a context manager - prevent Heartbeat timeout (discord.py)
        async with aiohttp.ClientSession() as session:
            async with session.post(llama2_url, json=payload) as response:

                if response.status == 200:
                    translated_text = (await response.json()).get("choices")[0].get("text")
                    # REQUEST_QUEUE.task_done()

                    context.append({"role": "user", "content": prompt})
                    context.append({"role": "bot", "content": translated_text})
                    context_handler.save_context(user_id, context)
                    print(f"Size of context: {len(context)}")

                    return translated_text
                else:
                    return "Sorry, there was an error with the translation."

    except Exception as e:
        return str(e)
    finally:
        #closing session when done
        response.close()

############################ C O M P L E T I O N ##############################
    
async def complete_text(prompt, user_id): 
    config = config_handler.get_config(user_id)
    context = context_handler.load_context(user_id)
    payload = {
        "prompt": f"\n\n### Complete the following:\n{prompt}\n\n### Response:\n",
            "stop": [
                "\n",
                "###"
            ],
            "max_tokens": config["complete_max_tokens"],
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(llama2_url, json=payload, timeout=180) as response:
                # print(f"Context: {context}")
                if response.status == 200:
                    completed_text = (await response.json()).get("choices")[0].get("text")

                    context.append({"role": "user", "content": prompt})
                    context.append({"role": "bot", "content": completed_text})
                    context_handler.save_context(user_id, context)
                    print(f"Size of context: {len(context)}")

                    return completed_text
                else:
                    return "Sorry, there was an error with the completion."
        
    except Exception as e:
        return str(e)
    finally:
        #closing session when done
        response.close()

########################## S U M M A R I Z A T I O N ##########################

async def summarize_text(prompt, user_id):
    config = config_handler.get_config(user_id)
    context = context_handler.load_context(user_id)
    payload = {
        "prompt": f"\n\n### Summarize the following:\n{prompt}\n\n### Response:\n",
            "stop": [
                "\n",
                "###"
            ], 
            "max_tokens": config["complete_max_tokens"],
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(llama2_url, json=payload) as response:
                # print(f"Context: {context}")

                if response.status == 200:
                    summarized_text = (await response.json()).get("choices")[0].get("text")
                    await asyncio.sleep(20)  

                    context.append({"role": "user", "content": prompt})
                    context.append({"role": "bot", "content": summarized_text}) 
                    context_handler.save_context(user_id, context)
                    print(f"Size of context: {len(context)}")

                    return summarized_text
                else:
                    return "Sorry, there was an error with the summarization."
        
    except Exception as e:
        return str(e)
    finally: 
        #closing session when done
        response.close()


#------------------------------------------------------------------------------
# Section 5: Bot Initialization
#------------------------------------------------------------------------------

# Explanation: Upon successful initialization, the bot reads the configured 
# intents and permissions and starts the Discord client, waiting for the first 
# events and messages to be received. The very last line of code is executing 
# the chatbot, which will run until it's quit or an unhandled error occurs.

@client.event
async def on_ready():
    print("Bot is ready")

############################## C O M M A N D S ################################

class HelpButtons(discord.ui.View): #HelpButtons class inherits from discord.ui.View
    def __init__(self): #Constructor Inheritance, initializes an instance of the HelpButtons class
        super().__init__() #invokes the constructor of the parent class (discord.ui.View)

############################ T R A N S L A T I O N ############################
    
    @discord.ui.button(label="Translate", style=discord.ButtonStyle.green)
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(content="Please provide the text to translate formatted as '<source language> <target language> <message>'\nEx: english german how are you.")
        try:
            response = await client.wait_for(
                "message",
                check=lambda m: m.author == interaction.user and m.channel == interaction.channel,
                # timeout=60.0  # Adjust the timeout as needed
            )
        except asyncio.TimeoutError:
            await interaction.followup.send("Translation request timed out.")
            return

        text_to_translate = response.content
        print(f"Received message: {text_to_translate} from {response.author}")

        user_id = str(response.author.id)

        source_language = text_to_translate.split(" ")[0]
        target_language = text_to_translate.split(" ")[1]
        text_to_translate = " ".join(text_to_translate.split(" ")[2:])

        # Call the translate_text function to get the translation
        translated_text = await translate_text(text_to_translate, source_language, target_language, user_id)

        # Send the translated text as a response
        await interaction.followup.send(f"Translation:\n {translated_text}", view=HelpButtons())


############################ C O M P L E T I O N ##############################


    @discord.ui.button(label="Complete", style=discord.ButtonStyle.red)
    async def button2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(content="Please provide the text to complete.")
        try:
            response = await client.wait_for(
                "message",
                check=lambda m: m.author == interaction.user and m.channel == interaction.channel,
                # timeout=60.0  # Adjust the timeout as needed
            )
        except asyncio.TimeoutError:
            await interaction.followup.send("Completion request timed out.")
            return
        
        text_to_complete = response.content
        print(f"Received message: {text_to_complete} from {response.author}")

        user_id = str(response.author.id)

        # Call the complete_text function to get the completion
        completed_text = await complete_text(text_to_complete, user_id)

        # Send the completed text as a response
        await interaction.followup.send(f"Completion:\n {completed_text}", view=HelpButtons())

######################### S U M M A R I Z A T I O N ###########################

    @discord.ui.button(label="Summarize", style=discord.ButtonStyle.blurple)
    async def button3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(content="Please provide the text to summarize.")
        try:
            response = await client.wait_for(
                "message",
                check=lambda m: m.author == interaction.user and m.channel == interaction.channel,
                # timeout=60.0  # Adjust the timeout as needed
            )
        except asyncio.TimeoutError:
            await interaction.followup.send("Summarization request timed out.")
            return
        
        text_to_summarize = response.content
        print(f"Received message: {text_to_summarize} from {response.author}")

        user_id = str(response.author.id)

        # Call the summarize_textfunction to get the summarize
        summarized_text = await summarize_text(text_to_summarize, user_id)

        # Send the summarize text as a response
        await interaction.followup.send(f"Summarization:\n {summarized_text}", view=HelpButtons())


######################### C O N F I G U R A T I O N ###########################

@client.tree.command()
async def botconfig(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    await interaction.response.send_modal(ConfigBotAIsettings(user_id))

@client.command()
async def button(ctx):
    message = await ctx.send("Welcome to the bot!", view=HelpButtons())
    ctx.view.message = message


@client.event 
async def on_message(message):
    is_dm = isinstance(message.channel, discord.channel.DMChannel)
    user_id = str(message.author.id)
    if message.author == client.user:
        return
    
    # Check if the user is in the user_contexts dictionary
    if user_id not in USER_CONTEXT:
        USER_CONTEXT[user_id] = []  # Initialize context data for this user in the channel

    
    if message.content.startswith("!reset"):
        reset_result = context_handler.reset_context(user_id)
        print(f"userID: {user_id}")
        print(f"Reset result: {reset_result}")

        #Avoiding sending an empty message
        if reset_result:
            await message.reply(reset_result, mention_author=True)
        return
    
    await client.process_commands(message)

client.run(TOKEN) 