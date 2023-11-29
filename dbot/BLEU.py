import nltk
import requests
import math
import asyncio
from bot import translate_text
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

# PROMPT
prompt = "The cat sat on the mat."
reference = "Die Katze saß auf der Matte."
source_language = "english"
target_language = "german"

# LLaMA2 API Endpoint
llama2_url = "http://127.0.0.1:8000/v1/completions/"

# Payload for the translation request
payload = {
    "prompt": f"\n\n### Translate the following from {source_language} to {target_language}:\n{prompt}\n\n### Response:\n",
    "stop": [
        "\n",
        "###"
    ],
    "max_tokens": 250,
}

async def main():
    # Make the translation request
    response = requests.post(llama2_url, json=payload)

    if response.status_code == 200:
        # Extract and process translation
        candidate_translation = response.json().get("choices")[0].get("text")
        print("Candidate Translation:", candidate_translation)
    else:
        print("Error:", response.status_code, response.text)

    # Tokenize the prompt
    reference_tokens = nltk.word_tokenize(reference)

    # Tokenize the candidate translation
    candidate_tokens = nltk.word_tokenize(candidate_translation)

    print("Reference Tokens:", reference_tokens)
    print("Candidate Tokens:", candidate_tokens)

    # Calculate BLEU score with smoothing
    smoother = SmoothingFunction().method1
    bleu_score = sentence_bleu([reference_tokens], candidate_tokens, smoothing_function=smoother)

    print("BLEU score:", bleu_score)

if __name__ == "__main__":
    asyncio.run(main())
