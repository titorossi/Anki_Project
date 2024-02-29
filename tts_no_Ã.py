from google.cloud import texttospeech

# Initialize the Google Cloud TTS client
client = texttospeech.TextToSpeechClient()

# Path to text file
text_file_path = r"C:\Users\titot\Desktop\PMW\Anki_Project\Texts\phrase_no_Ã.txt"

# Function to generate audio file
def generate_audio(phrase, file_number):
    synthesis_input = texttospeech.SynthesisInput(text=phrase)
    voice = texttospeech.VoiceSelectionParams(
        language_code="it-IT", name="it-IT-Neural2-C"
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3)
    
    # Perform TTS request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config)
    
    # Define the output file path
    output_file_path = rf"C:\Users\titot\Desktop\PMW\Anki_Project\audio_no_Ã\phrase_{file_number}.mp3"
    
    # Write the response's audio content to the output file
    with open(output_file_path, 'wb') as output_file:
        output_file.write(response.audio_content)
        print(f'Audio written to file: "{output_file_path}"')

# Read the text file and process each line
with open(text_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        phrase, number = line.rsplit(' ', 1)
        generate_audio(phrase, number.strip())

print("Audio generation complete.")