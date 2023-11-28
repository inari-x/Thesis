#-------------------------------------------------------------------------------------------------
# Project: Discord Bot in Python
# Description: A Discord bot that can be used to chat with users in a server.
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------------------------
import json
import config_handler
import os #file handling

from pathlib import Path

#-------------------------------------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------------------------------------

CONTEXT_DIRECTORY = "saved-context"

#-------------------------------------------------------------------------------------------------  
# Functions
#-------------------------------------------------------------------------------------------------

# Returns the filename of the context file for the given user id
def context_filename(user_id): #context_id is a user/context is saved by user 
    ctx_fn = os.path.join(os.getcwd(), CONTEXT_DIRECTORY, str(user_id) + ".json") #because of virtual environment os.getcwd()
    # print(ctx_fn)
    return ctx_fn

import json

# Returns the context for the given user id
def load_context(user_id):
    config = config_handler.get_config(user_id)
    messages = []
    if Path(context_filename(user_id)).is_file():
        with open(context_filename(user_id), "r") as f:
            try:
                messages = json.loads(f.read())
            except json.JSONDecodeError:
                print(f"Error: The file {context_filename(user_id)} does not contain valid JSON.")
                messages = [{"role": "system", "content": config["system_prompt"]}]
    else:
        messages = [{"role": "system", "content": config["system_prompt"]}]
    return messages

# Saves the context for the given user id
def save_context(user_id, messages):
	with open(context_filename(user_id), "w") as f:
		f.write(json.dumps(messages))
	return

# Resets the context for the given user id
def reset_context(user_id):
      context_file_path = context_filename(user_id)
      if Path(context_file_path).is_file():
        try:
            os.remove(context_filename(user_id))
            return "Context Reset"
        except FileNotFoundError:
             return "Context file doesn't exist"

