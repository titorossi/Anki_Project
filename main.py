from text_speech import synthesize_speech
from gpt_to_ita import generate_phrase_and_translate
from word_reader import read_words_from_file
from anki_template import create_anki_model
from anki_paste import add_note, upload_audio_to_anki

# Create Anki model and replace "your_model_name" with the name of your model
create_anki_model("your_model_name")

# Read words from file
file_path = r"C:\Users\titot\Desktop\PMW\Anki_Project\Texts\3_words.txt"
words = read_words_from_file(file_path)

# Set language
language = "Italian"

# Generate phrases and translations
for i, word in enumerate(words):
    word, generated_phrase, translated_word, translated_phrase, word_definition = generate_phrase_and_translate(word, language)
    print(f"Word: {word}")
    print(f"Generated phrase: {generated_phrase}")
    print(f"Translated word: {translated_word}")
    print(f"Translated phrase: {translated_phrase}")
    print(f"Word definition: {word_definition}")
    
    # Synthesize speech returns the binary audio content
    word_audio = synthesize_speech(word)
    phrase_audio = synthesize_speech(generated_phrase)

    # Upload audio files to Anki's media library
    word_audio_file = upload_audio_to_anki(f"word_{i}.mp3", word_audio)
    phrase_audio_file = upload_audio_to_anki(f"phrase_{i}.mp3", phrase_audio)
    
    fields = {
        "Native word": translated_word,
        "Native phrase": translated_phrase,
        "Foreign word": word,
        "Foreign word audio": f"[sound:{word_audio_file}]",
        "Foreign phrase": generated_phrase,
        "Foreign phrase audio": f"[sound:{phrase_audio_file}]",
        "Definition": word_definition
    }

    add_note("deckname", "your_model_name", fields)
