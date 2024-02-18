import requests
import json
import base64

def invoke(action, params={}):
    request_json = json.dumps({'action': action, 'params': params, 'version': 6})
    response = requests.post('http://localhost:8765', data=request_json)
    return response.json()

def upload_audio_to_anki(filename, audio_content):
    encoded_audio = base64.b64encode(audio_content).decode('utf-8')
    params = {
        "filename": filename,
        "data": encoded_audio
    }
    invoke('storeMediaFile', params)
    return filename

def add_note(deck_name, model_name, fields):
    note = {
        "deckName": deck_name,
        "modelName": model_name,
        "fields": fields,
        "options": {
            "allowDuplicate": False
        },
        "tags": []
    }
    invoke('addNote', {'note': note})

# Example usage:
fields = {
    "Native word": "ciao",
    "Native phrase": "Ciao, come stai?",
    "Definition": "A common Italian greeting.",
    "Foreign word": "hello",
    "Foreign word audio": "[sound:example_audio.mp3]",
    "Foreign phrase": "Hello, how are you?",
    "Foreign phrase audio": "[sound:example_audio.mp3]"
}
add_note("test", fields)
