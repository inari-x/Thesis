import pytest
import time
from unittest.mock import patch
from bot import translate_text, complete_text, summarize_text

user_id = '1128758613062717450' #my user id

# -----------------------------------------------------------------------------
# BOT.PY UNIT TESTS
# -----------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_translate_text():
    # Mock the requests.post function to return a predefined response
    with patch('bot.requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"choices": [{"text": "Translated text"}]}
   
        start_time = time.time()

        # Call function
        await translate_text("Hello", "en", "fr", user_id)
        end_time = time.time()

        # Print access time
        print(f"Translate Text Access Time: {end_time - start_time} seconds")

@pytest.mark.asyncio
async def test_complete_text():
    # Mock the requests.post function to return a predefined response
    with patch('bot.requests.post') as mock_post:
        mock_post.return_value.statu_code = 200
        mock_post.return_value.json.return_value = {"choices": [{"text": "Completed text"}]}

        start_time = time.time()

        # Call function
        await complete_text("Hello I am ", user_id)
        end_time = time.time()

        print(f"Complete Text Access Time: {end_time - start_time} seconds")

@pytest.mark.asyncio
async def test_summarize_text():
    # Mock the requests.post function to return a predefined response
    with patch('bot.requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"choices": [{"text": "Summarized text"}]}

        start_time = time.time()

        # Call function
        await summarize_text("Hello my name is Katrin, I am 25 years old", user_id)
        end_time = time.time()

        print(f"Summarize Text Access Time: {end_time - start_time} seconds")

