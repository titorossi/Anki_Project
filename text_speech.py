from google.cloud import texttospeech

def synthesize_speech(text, client=None):
    # Instantiates a client if not provided
    if client is None:
        client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the desired language code ("it-IT") and the ssml
    voice = texttospeech.VoiceSelectionParams(
        language_code="it-IT", name="it-IT-Chirp3-HD-Autonoe"
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

    # Return the audio content
    return response.audio_content
