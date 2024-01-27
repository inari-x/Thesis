# import nltk
# import requests
# import math
# import asyncio
# from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

# source_language="english"
# target_language="german"

# # Translation pairs for different domains
# translation_pairs = {
#     "Technology": [
#         ("The new algorithm can significantly improve the accuracy of machine translation.",
#          "Der neue Algorithmus kann die Genauigkeit der maschinellen Übersetzung erheblich verbessern."),
#         ("The development of artificial intelligence has led to major advancements in natural language processing.",
#          "Die Entwicklung der künstlichen Intelligenz hat zu bedeutenden Fortschritten in der natürlichen Sprachverarbeitung geführt."),
#         ("The blockchain technology has the potential to revolutionize various industries.",
#          "Die Blockchain-Technologie hat das Potenzial, verschiedene Branchen zu revolutionieren.")
#     ],
#     "Science": [
#         ("The Earth's atmosphere is composed of various gases, including nitrogen, oxygen, and argon.",
#          "Die Erdatmosphäre besteht aus verschiedenen Gasen, darunter Stickstoff, Sauerstoff und Argon."),
#         ("The theory of relativity explains the relationship between space and time.",
#          "Die Relativitätstheorie erklärt die Beziehung zwischen Raum und Zeit."),
#         ("The discovery of water on Mars has significant implications for astrobiology.",
#          "Die Entdeckung von Wasser auf dem Mars hat bedeutende Auswirkungen auf die Astrobiologie.")
#     ],
#     "Literature": [
#         ("In the depths of the forest, a hidden village thrived.",
#          "In den Tiefen des Waldes gedieh ein verborgenes Dorf."),
#         ("The protagonist's journey was filled with challenges and triumphs.",
#          "Die Reise des Protagonisten war voller Herausforderungen und Triumphe."),
#         ("The author's words painted vivid images in the reader's mind.",
#          "Die Worte des Autors malten lebendige Bilder in den Köpfen der Leser.")
#     ]
# }

# # LLaMA2 API Endpoint
# llama2_url = "http://127.0.0.1:8000/v1/completions/"

# # Payload for the translation request
# payload = {
#     "stop": [
#         "\n",
#         "###"
#     ],
#     "max_tokens": 250,
# }

# async def calculate_bleu(prompt, reference, smoother):
#     # Payload for the translation request
#     payload["prompt"] = f"\n\n### Translate the following from {source_language} to {target_language}:\n{prompt}\n\n### Response:\n"

#     # Make the translation request
#     response = requests.post(llama2_url, json=payload)

#     if response.status_code == 200:
#         # Extract and process translation
#         candidate_translation = response.json().get("choices")[0].get("text")

#         print(f"Candidate translation: {candidate_translation}")

#         # Tokenize the reference and candidate translations
#         reference_tokens = nltk.word_tokenize(reference)
#         candidate_tokens = nltk.word_tokenize(candidate_translation)

#         print(f"Reference tokens: {reference_tokens}")
#         print(f"Candidate tokens: {candidate_tokens}")

#         # Calculate BLEU score
#         bleu_score = sentence_bleu([reference_tokens], candidate_tokens, smoothing_function=smoother)
#         return bleu_score

#     else:
#         print("Error:", response.status_code, response.text)
#         return 0

# async def main():
#     cumulative_bleu = 0
#     smoother = SmoothingFunction().method1
#     total_translations = 0

#     for domain, prompts in translation_pairs.items():
#         print(f"Domain: {domain}")
#         for prompt, reference in prompts:
#             bleu_score = await calculate_bleu(prompt, reference, smoother)
#             print(f"Prompt: {prompt}")
#             print(f"Reference: {reference}")
#             print(f"BLEU score: {bleu_score}")
#             cumulative_bleu += bleu_score
#             total_translations += 1

#     normalized_bleu = cumulative_bleu / total_translations
#     print(f"\nCumulative BLEU score for all prompts: {normalized_bleu}")

# if __name__ == "__main__":
#     asyncio.run(main())
