from google.cloud import texttospeech

# Instantiates a client
client = texttospeech.TextToSpeechClient()

# Set the text input to be synthesized
synthesis_input = texttospeech.SynthesisInput(text="Italiano é veramente una bella lingua, e facile da imparare.")

# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
voice = texttospeech.VoiceSelectionParams(
    language_code="it-IT", name="it-IT-Neural2-C"
)

# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

# Specify the full path where you want to save the file
output_file_path = r"C:\Users\titot\Desktop\PMW\Anki_Project\google_tts_tests\output.mp3"

# The response's audio_content is binary.
with open(output_file_path, "wb") as out:
    # Write the response to the output file.
    out.write(response.audio_content)
    print(f'Audio content written to file "{output_file_path}"')
