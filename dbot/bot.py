import asyncio
import discord
from discord.ext import commands 
import os
import datetime

import context_handler

from request_queue import llm_complete_request, init_request_queue
# Import your llm_completions module here
import llm_completions

from dotenv import load_dotenv



load_dotenv()
TOKEN = os.getenv("TOKEN")

class MyClient(discord.Client):
    async def on_ready(self):
        await init_request_queue()
        print('Current time: ', datetime.datetime.now())
        print(f'User: {self.user} (ID: {self.user.id})')
        print('Warming up...')

    async def on_message(self, message):
        is_dm = isinstance(message.channel, discord.channel.DMChannel)
        at_mention = f'<@{self.user.id}>'
        context_id = str(message.channel)
        if is_dm:
            context_id = str(message.author.id)
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        # If message is DM or @sandbox
        if is_dm or message.content.startswith(at_mention):
            # console log here
            print(f"Received message: {message.content} from {message.author}")
            stripped_message = str(message.content).replace(at_mention, '').strip()
            if stripped_message.startswith("!reset"):
                reset_result = context_handler.reset_context(context_id)
                await message.reply(reset_result, mention_author=True)
                return
            if stripped_message.startswith("!complete"):
                complete_response = await llm_complete_request(stripped_message, context_id, complete_only=True)
                await message.reply(complete_response, mention_author=True)
                return
            complete_response = await llm_complete_request(stripped_message, context_id, complete_only=False)
            await message.reply(complete_response, mention_author=True)
            
        # add a function for !help with an embedded message
        if message.content.startswith("!help"):
            embed = discord.Embed(title="Help", description="List of my commands are:", color=0xeee657)

            embed.add_field(name="!help", value="Gives this message.", inline=False)
            embed.add_field(name="!complete", value="Completes the given sentence.\n!complete <to be determined>", inline=False)
            embed.add_field(name="!translate", value="Command parameters are source language, origin language and message.\n!translate german english bitte", inline=False)
            embed.add_field(name="!enhance", value="Command parameters are method and message.\n!enhance \"make simpler\" We are not particulary engaged at this time", inline=False)
            
            # add a discord.Button to the embed 
            # button_1 = discord.ui.Button(label="Translate", url="https://google.com")
            # button_2 = discord.ui.Button(label="Complete", url="https://google.com")
            # button_3 = discord.ui.Button(label="Enhance", url="https://google.com")



            # add button1, button2 and button3 to the embed as components
            # action_row = discord.ActionRow(button_1, button_2, button_3)
            #ActionRow takes children as a list of components and type 

            #                              children                         type
            # discord.ActionRow( [button_1, button_2, button_3], type=discord.ComponentType.action_row)

            # add action_row to the embed

            embed.set_footer(text="Click the button to go to the website")
            embed.set_thumbnail(url="https://i.imgur.com/axLm3p6.png")
            embed.set_author(name="LLM Bot", url="", icon_url="https://i.imgur.com/axLm3p6.png")
            embed.add_field(name="Website (google.com)", value="https://google.com", inline=False)
            

            # await message.channel.send(embed=embed, components=[action_row])
            await message.channel.send(embed=embed)

intents = discord.Intents.default()
intents.message_content = True
# # add ! prefix to bot commands




client = MyClient(intents=intents)
client.run(TOKEN)

