#-----------------------------------------------------------------------------
# Description:
# This file contains functions for handling the configuration of the AI
# assistant. The configuration is stored in a JSON file in the configs
# directory. The configuration is loaded into memory when the AI assistant
# starts up and is updated in memory when the configuration is changed.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
import json
import os

#-----------------------------------------------------------------------------
# Constants
#-----------------------------------------------------------------------------

CONFIG_DIRECTORY = "./configs"
CONFIGS = {}
DEFAULT_CONFIG = {

    "system_prompt": "You are an AI assistant",
    "max_tokens": 256,
    "complete_max_tokens": 512
}

#-----------------------------------------------------------------------------
# Functions
#-----------------------------------------------------------------------------

# Returns the filename of the config file for the given context id
def get_config_filename(context_id):
    return os.path.join(CONFIG_DIRECTORY, str(context_id) + ".json")

# Returns the config for the given context id
def get_config(context_id):
    if CONFIGS.get(context_id, None):
        with open(os.path.join(CONFIG_DIRECTORY, str(context_id) + ".json"), 'r') as f:
            config = json.loads(f.read())
            CONFIGS[context_id] = config #Update config in memory
            return config
        
    config = DEFAULT_CONFIG
    save_config(context_id, config)
    return config

# Saves the config for the given context id 
def save_config(context_id, config):
    CONFIGS[context_id] = config
    config_filename = os.path.join(CONFIG_DIRECTORY, str(context_id) + ".json")
    with open(config_filename, 'w') as f:
        f.write(json.dumps(config))
    

