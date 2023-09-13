import asyncio

import llm_completions

REQUEST_QUEUE =	asyncio.Queue()
RESPONSE_QUEUE = asyncio. Queue()

async def queue_worker():
	while True:
		item = await REQUEST_QUEUE.get()
		question, context_id, complete_only = item
		if complete_only:
			complete_output = await llm_completions.llm_complete(question)
		else:
			complete_output = await llm_completions.llm_chat_complete(question, context_id)

		REQUEST_QUEUE.task_done()
		await RESPONSE_QUEUE.put(complete_output)

async def llm_complete_request(question, context_id, complete_only=False):
	item = (question, context_id, complete_only)
	await REQUEST_QUEUE.put(item)
	completion = await RESPONSE_QUEUE.get()
	RESPONSE_QUEUE.task_done()
	return completion

async def init_request_queue():
	await asyncio.create_task(queue_worker())
