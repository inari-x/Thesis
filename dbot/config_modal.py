#------------------------------------------------------------------------------
# Description: This file contains the ConfigBotAIsettings class, which is a 
# subclass of discord.ui.Modal. This class is used to create a modal that 
# allows the user to change the settings for the AI bot.
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

import config_handler
import discord
from discord import ui
import logging

#------------------------------------------------------------------------------
# ConfigBotAIsettings class
#------------------------------------------------------------------------------

class ConfigBotAIsettings(discord.ui.Modal):
    def __init__(self, context_id):
        super().__init__(title="Channel AI Bot Settings")
        self.chat_context_id = context_id
        self.config = config_handler.get_config(context_id)
        
        # Define and initialize the UI elements within the __init__ method
        self.max_tokens_field = discord.ui.TextInput(
            label="Max Tokens", 
            default=str(self.config["max_tokens"]),
        )

        self.complete_max_tokens_field = discord.ui.TextInput(
            label="Completion Max Tokens", #
            default=str(self.config["complete_max_tokens"]),
        )

        self.system_prompt_field = discord.ui.TextInput(
            label="System Prompt",
            style=discord.TextStyle.long,
            default=self.config["system_prompt"],
            max_length=1000
        )
        
        # Set the body of the modal
        self.add_item(self.max_tokens_field)
        self.add_item(self.complete_max_tokens_field)
        self.add_item(self.system_prompt_field)

#------------------------------------------------------------------------------
# Methods
#------------------------------------------------------------------------------

    # This method is called when the user clicks the submit button
    async def on_submit(self, interaction):
        old_system_prompt = self.config["system_prompt"]
        config = {
            "max_tokens": self.max_tokens_field.value, 
            "complete_max_tokens": self.complete_max_tokens_field.value, 
            "system_prompt": self.system_prompt_field.value #system prompt is where the user 
        }
        config_handler.save_config(self.chat_context_id, config)

        await interaction.response.send_message(f"Config updated.", ephemeral=True)

        if old_system_prompt != config["system_prompt"]:
            await interaction.channel.send("System prompt changed. Resetting context for another config", silent=True)
    
    # This method is called when the user clicks the cancel button
    async def on_error(self, interaction, error):
        logger = logging.getLogger("discord")
        error_msg = f"Error in ConfigBotAIsettings.on_submit: {error}"
        logger.error(error_msg)
        await interaction.response.send_message(error_msg, ephemeral=True)
