import json
import os

CONFIG_DIRECTORY = "./configs"
CONFIGS = {}
DEFAULT_CONFIG = {

    "system_prompt": "You are an AI assistant",
    "max_tokens": 256,
    "complete_max_tokens": 512
}

def get_config_filename(context_id):
    return os.path.join(CONFIG_DIRECTORY, str(context_id) + ".json")

def get_config(context_id):
    if CONFIGS.get(context_id, None):
        with open(os.path.join(CONFIG_DIRECTORY, str(context_id) + ".json"), 'r') as f:
            config = json.loads(f.read())
            CONFIGS[context_id] = config #Update config in memory
            return config
        
    config = DEFAULT_CONFIG
    save_config(context_id, config)
    return config
    
def save_config(context_id, config):
    CONFIGS[context_id] = config
    config_filename = os.path.join(CONFIG_DIRECTORY, str(context_id) + ".json")
    with open(config_filename, 'w') as f:
        f.write(json.dumps(config))
    

