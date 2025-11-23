import google.generativeai as genai
import os
from concurrent.futures import ThreadPoolExecutor
import time

def generate_phrase_and_translate(word, language, model=None):
    # Configure Gemini API and create model if not provided
    if model is None:
        genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
        model = genai.GenerativeModel('gemini-2.5-flash')

    # Define all 4 prompts
    phrase_prompt = f"""Generate a concise, natural {language} phrase (5-12 words) using the word '{word}' at CEFR B1-B2 level.

Requirements:
- Use intermediate vocabulary and common grammatical structures
- Make it conversational and practical
- Keep it brief and clear
- Use the word naturally (conjugate verbs as needed)
- Return ONLY the {language} phrase, nothing else"""
    
    # Helper function to make API call with retry logic
    def call_api_with_retry(prompt, max_retries=3):
        for attempt in range(max_retries):
            try:
                response = model.generate_content(prompt)
                return response.text.strip()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                wait_time = (2 ** attempt) * 1  # Exponential backoff: 1s, 2s, 4s
                time.sleep(wait_time)
        return ""
    
    # First, generate the phrase (needed for subsequent calls)
    generated_phrase = call_api_with_retry(phrase_prompt)
    
    # Now make the 3 remaining calls in parallel
    phrase_translation_prompt = f"Translate this {language} phrase to natural English: {generated_phrase}\n\nProvide ONLY the English translation, nothing else."
    word_translation_prompt = f"Translate this {language} word to English: {word}\n\nProvide ONLY the English translation (one or two words), nothing else."
    definition_prompt = f"""Provide a concise {language} dictionary definition for '{word}' suitable for CEFR B1-B2 learners.

Requirements:
- Write in clear, intermediate-level {language}
- Keep it brief (1-2 sentences maximum)
- Do NOT include the word itself in the definition
- Do NOT add notes or examples
- Return ONLY the definition"""
    
    # Execute the 3 remaining API calls in parallel
    with ThreadPoolExecutor(max_workers=3) as executor:
        phrase_translation_future = executor.submit(call_api_with_retry, phrase_translation_prompt)
        word_translation_future = executor.submit(call_api_with_retry, word_translation_prompt)
        definition_future = executor.submit(call_api_with_retry, definition_prompt)
        
        translated_phrase = phrase_translation_future.result()
        translated_word = word_translation_future.result()
        word_definition = definition_future.result()
    
    # Small delay to avoid overwhelming API (4 calls per word × delay = requests spread over time)
    time.sleep(0.3)

    return word, generated_phrase, translated_word, translated_phrase, word_definition