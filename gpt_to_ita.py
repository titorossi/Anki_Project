from openai import OpenAI
import random

def generate_phrase_and_translate(word, language):
    client = OpenAI()

    # Generate a random number to determine whether the word will be conjugated or not
    conjugation_choice = random.randint(0, 3)

    # Define the conjugation instruction based on the random number
    if conjugation_choice == 0:
        # 0 means no conjugation
        conjugation_instruction = f"In '{language}', generate a phrase using the given word without conjugation. Generate only the phrase in the given language, do not provide anything else."
    else:
        # 1, 2, 3 mean random conjugation
        conjugation_instruction = f"In '{language}', generate a phrase using the given word, if the word is a verb, give it a random conjugation. Generate only the phrase in the given language, do not provide anything else."

    # Generate a phrase using the word in the desired foreign language
    phrase_completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": conjugation_instruction},
        {"role": "user", "content": f"Generate a phrase using '{word}'."}
      ]
    )
    generated_phrase = phrase_completion.choices[0].message.content

    # Translate the phrase into English
    translation_completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "Translate the following phrase into English. Do not provide anything else."},
        {"role": "user", "content": generated_phrase}
      ]
    )
    translated_phrase = translation_completion.choices[0].message.content

    # Get dictionary definition of the word in the desired foreign language
    definition_completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": f"Provide a dictionary definition of the given word in '{language}'. Do not include the word in the definition and do not include any notes, provide only the definition."},
        {"role": "user", "content": f"Define '{word}'."}
      ]
    )
    word_definition = definition_completion.choices[0].message.content

    return word, generated_phrase, translated_phrase, word_definition