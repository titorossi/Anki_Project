from text_speech import synthesize_speech
from gpt_to_ita import generate_phrase_and_translate
from word_reader import read_words_from_file

file_path = r"C:\Users\titot\Desktop\PMW\Anki_Project\Texts\3_words.txt"
words = read_words_from_file(file_path)

language = "Italian"


for i, word in enumerate(words):
    word, generated_phrase, translated_phrase, word_definition = generate_phrase_and_translate(word, language)
    print(f"Word: {word}")
    print(f"Generated phrase: {generated_phrase}")
    print(f"Translated phrase: {translated_phrase}")
    print(f"Word definition: {word_definition}")
    
    word_audio = synthesize_speech(word)
    phrase_audio = synthesize_speech(generated_phrase)
    
    with open(f"word_{i}.mp3", "wb") as out:
        out.write(word_audio)
        
    with open(f"phrase_{i}.mp3", "wb") as out:
        out.write(phrase_audio)
