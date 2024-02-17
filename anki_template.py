import requests
import json

def create_anki_model():
    #Replace the model_name with your desired model name
    model_name = "your_model_name"
    field_names = ["Native word", "Native phrase", "Foreign word", "Foreign word audio", "Foreign phrase", "Foreign phrase audio", "Definition"]

    # Front and back for the productive cards
    front_html = """
    {{Native word}}<br>
    <div class="line"></div>
    {{Native phrase}}

    {{#Definition}}
        <div class="toggle-content" onclick="toggleShow(this)">
            <p class="trigger">[ Definition ]</p>
            <p class="payload">{{Definition}}</p>
        </div>
        <script>
            function toggleShow(element) {
                element.classList.toggle('shown');
            }
        </script>
    {{/Definition}}
    """
    back_html = """
    {{FrontSide}}

    <hr id=answer>

    {{Foreign word}}<br>
    {{Foreign word audio}}<br>
    <div class="line"></div>
    {{Foreign phrase}}<br>
    {{Foreign phrase audio}}

    {{#Definition}}<p>{{Definition}}</p>{{/Definition}}

    <hr>
    """

    # Front and back for the receptive cards
    front_html_2 = """
    {{Foreign word}}<br>
    {{Foreign word audio}}


        <div class="toggle-content" onclick="toggleShow(this)">
            <p class="trigger">[ Phrase ]</p>
            <p class="payload">{{Foreign phrase}}<br>{{Foreign phrase audio}}</p>
        </div>
        <script>
            function toggleShow(element) {
                element.classList.toggle('shown');
            }
        </script>
    """
    back_html_2 = """
    {{FrontSide}}

    <hr id=answer>

    {{Native word}}<br>
    <div class="line"></div>
    {{Native phrase}}

    <p>{{Foreign phrase}}<br>{{Foreign phrase audio}}</p>

    <hr>
    """

    css = """
    .card {
        font-family: arial;
        font-size: 20px;
        text-align: center;
        color: black;
        background-color: white;
    }

    .card { 
        font: 1.5em/1.5 sans-serif; 
        text-align: center; 
    }

    .toggle-content {
        background: #f2fbe7; 
        border: 1px solid #dff5c4; 
        border-radius: 6px; 
        color: #7a876b; 
        cursor: pointer;
    }

    .toggle-content:hover {
        background: #dff5c4; 
        color: #000;
    }

    .toggle-content .payload {
        display: none;
    }

    .toggle-content.shown {
        background: #fff; 
        color: #000;
    }

    .toggle-content.shown .payload {
        display: block;
        max-height: 150px;
        overflow-y: auto;
    }

    .line { 
        width: 50%; 
        margin: 0 auto; 
        border-top: 1px solid black; 
    }
    """
    # The payload for the request
    payload = {
        "action": "createModel",
        "version": 6,
        "params": {
            "modelName": model_name,
            "inOrderFields": field_names,
            "css": css,
            "cardTemplates": [
                {
                    "Name": "Productive",
                    "Front": front_html,
                    "Back": back_html
                },
                {
                    "Name": "Receptive",
                    "Front": front_html_2,
                    "Back": back_html_2
                }
            ]
        }
    }
    response = requests.post('http://localhost:8765', json=payload)
    return response.json()
