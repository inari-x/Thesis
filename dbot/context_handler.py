import json
import os

from pathlib import Path

CONTEXT_DIRECTORY = "./saved-context"

def context_filename(context_id):
	ctx_fn = os.path.join(CONTEXT_DIRECTORY, str(context_id) + ".json")
	return ctx_fn

def load_context(context_id):
	if Path(context_filename(context_id)).is_file():
		with open(context_filename(context_id), "r") as f:
			messages = json.loads(f.read())

		return messages

	messages = [
		{"role": "system", "content":"You are an AI assistant"}
	]
	return messages


def save_context(context_id, messages):
	with open(context_filename(context_id), "w") as f:
		f.write(json.dumps(messages))
	return

def reset_context(context_id):
	try:
		os.remove(context_filename(context_id))
		return "Context Reset"
	except FileNotFoundError:
		return "Context file doesn't exist"

