from pathlib import Path
import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock, Mock
from bot import REQUEST_QUEUE_COMPLETION, REQUEST_QUEUE_SUMMARIZATION, REQUEST_QUEUE_TRANSLATION, RESPONSE_QUEUE_COMPLETION, RESPONSE_QUEUE_SUMMARIZATION, RESPONSE_QUEUE_TRANSLATION, HelpButtons, MyClient, botconfig, button, init_request_queues, on_message, queue_worker, setup_hook, translate_text, complete_text, summarize_text
from context_handler import load_context, save_context, reset_context, context_filename
from config_handler import get_config, save_config

user_id = '1128758613062717450' #my user id

# -------------------------------------------------------------------------------------------------
# BOT.PY UNIT TESTS
# -------------------------------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_translate_text():
    # Mock the requests.post function to return a predefined response
    with patch('bot.requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"choices": [{"text": "Translated text"}]}

        # Call function
        result, request_type = await translate_text("Hello", "en", "fr", user_id)

        # Check if the function returns the expected result
        assert result == "Translated text"
        assert request_type == "translation"

@pytest.mark.asyncio
async def test_complete_text():
    # Mock the requests.post function to return a predefined response
    with patch('bot.requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"choices": [{"text": "Completed text"}]}

        # Call function
        result, request_type = await complete_text("Hello I am ", user_id)

        # Check if the function returns the expected result
        assert result == "Completed text"
        assert request_type == "completion"

@pytest.mark.asyncio
async def test_summarize_text():
    # Mock the requests.post function to return a predefined response
    with patch('bot.requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"choices": [{"text": "Summarized text"}]}

        # Call function
        result, request_type = await summarize_text("Hello my name is Katrin, I am 25 years old", user_id)

        # Check if the function returns the expected result
        assert result == "Summarized text"
        assert request_type == "summarization"

@pytest.mark.asyncio
async def test_load_context():
    # Set up any necessary context or user data
    
    # Call the function
    context = load_context(user_id)
    
    # Assert that the context is what you expect
    assert isinstance(context, list)

@pytest.mark.asyncio
async def test_save_context():
    # Set up any necessary context or user data
    messages = [{"role": "user", "content": "Hello"}]
    
    # Call the function
    save_context(user_id, messages)
    
    # Assert that the context file exists and has been saved correctly
    assert Path(context_filename(user_id)).is_file()


# #command testing
@pytest.mark.asyncio
#test !reset, .botconfig, .button

async def test_reset():
    # Set up any necessary context or user data
    messages = [{"role": "user", "content": "Hello"}]

    ### STUCK HERE WITH USER FILE DOES NOT EXIST BUT STILL IS DELETED
    result = reset_context(user_id)
    print(result)

    #wait to allow file deletion
    await asyncio.sleep(1)
    
    # Assert that the context file has been deleted
    assert not Path(context_filename(user_id)).is_file()

@pytest.mark.asyncio
async def test_botconfig():
    # Set up any necessary context or user data
    
    # Call the function
    context = load_context(user_id)

    print(context)
    
    # Assert that the context is what you expect
    assert isinstance(context, list)

@pytest.mark.asyncio
async def test_button():
    # Set up any necessary context or user data
    
    # Call the function
    context = load_context(user_id)

    print(context)
    
    # Assert that the context is what you expect
    assert isinstance(context, list)
