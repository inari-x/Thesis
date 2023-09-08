import asyncio
import openai

import context_handler

openai.api_key = "wedontneedit"
openai.api_base = "http://127.0.0.1:8000/v1"

def get_model():
	models = openai.Model.list()
	return models["data"][0]["id"]

async def llm_complete(message):
	completion_resp = await openai.Completion.acreate(
		model=get_model(),
                prompt=message,
                max_tokens=512
                ) 
	return f"{completion_resp['choices'][0]['text']}"

async def llm_chat_complete(prompt, context_id):
	messages = context_handler.load_context(context_id)
	messages = [message for message in messages if "role" in message and message["role"] != "comment"]
	message = {"role": "user", "content": prompt}
	messages.append(message)
	tokens_exceeded = True
	while tokens_exceeded:
		try:
			chat_completion_resp = await openai.ChatCompletion.acreate(
				model=get_model(),
				messages=messages,
				max_tokens=256
				)
			tokens_exceeded = False
		
		except openai.error.APIError:
			messages.pop(1)
			
	response = chat_completion_resp.choices[0].message
	response_msg = response.get("content")
	messages.append(response.to_dict())
	context_handler.save_context(context_id, messages)

	return f"{response_msg}"

async def cli_chat():
	while True:
		question = input("User:")
		response_msg = await llm_chat_complete(question, "cli-chat")
		print(response_msg)


if __name__ == "__main__":
	asyncio.run(cli_chat())

