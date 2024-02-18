import requests
import json
import base64

# Send a request to the AnkiConnect API
def invoke(action, params={}):
    request_json = json.dumps({'action': action, 'params': params, 'version': 6})
    response = requests.post('http://localhost:8765', data=request_json)
    return response.json()

# Create a new deck in Anki
def create_deck(deck_name):
    invoke('createDeck', {'deck': deck_name})

# Upload an audio file to Anki's media library
def upload_audio_to_anki(filename, audio_content):
    encoded_audio = base64.b64encode(audio_content).decode('utf-8')
    params = {
        "filename": filename,
        "data": encoded_audio
    }
    invoke('storeMediaFile', params)
    return filename

# Add a note to Anki
def add_note(deck_name, model_name, fields):
    note = {
        "deckName": deck_name,
        "modelName": model_name,
        "fields": fields,
        "options": {
            "allowDuplicate": True
        },
        "tags": []
    }
    return invoke('addNote', {'note': note})
