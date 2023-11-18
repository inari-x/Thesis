import json
import config_handler
import os #file handling

from pathlib import Path

CONTEXT_DIRECTORY = "./saved-context"

def context_filename(user_id): #context_id is a user/context is saved by user
	ctx_fn = os.path.join(CONTEXT_DIRECTORY, str(user_id) + ".json")
	return ctx_fn

import json

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


def save_context(user_id, messages):
	with open(context_filename(user_id), "w") as f:
		f.write(json.dumps(messages))
	return

def reset_context(user_id):
	try:
		os.remove(context_filename(user_id))
		return "Context Reset"
	except FileNotFoundError:
		return "Context file doesn't exist"

