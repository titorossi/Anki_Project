from pathlib import Path
import openai

# Set your API key
openai.api_key = ''

# Create a file to store the audio and generate the audio
speech_file_path = Path(__file__).parent / "speech_shimmer.mp3"
response = openai.audio.speech.create(
  model="tts-1",
  voice="shimmer",
  input="Italiano é veramente una bella lingua, e facile da imparare."
)
response.stream_to_file(speech_file_path)
