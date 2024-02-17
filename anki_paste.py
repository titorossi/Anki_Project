import requests
import json

def invoke(action, params={}):
    request_json = json.dumps({'action': action, 'params': params, 'version': 6})
    response = requests.post('http://localhost:8765', data=request_json)
    return response.json()

def add_note(deck_name, fields):
    note = {
        "deckName": deck_name,
        "modelName": "your_model_name",
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
