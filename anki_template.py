import requests
import json

def create_anki_model(model_name, front_html, back_html, css):
    payload = {
        "action": "createModel",
        "version": 6,
        "params": {
            "modelName": model_name,
            "inOrderFields": field_names,
            "css": css,
            "cardTemplates": [
                {
                    "Name": "Card 1",
                    "Front": front_html,
                    "Back": back_html
                }
            ]
        }
    }
    response = requests.post('http://localhost:8765', json=payload)
    return response.json()

# Replace 'your_model_name' with the desired name of your Anki model
model_name = "your_model_name"
field_names = ["Native word", "Native phrase", "Foreign word", "Foreign phrase", "Foreign phrase audio", "Definition"]
front_html = """
{{Native word}}<br>
<div class="line"></div>
{{Native phrase}}

{{#Definition}}
    <div class="definition" onclick="toggleShow(this)">
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
<div class="line"></div>
{{Foreign phrase}}<br>
{{Foreign phrase audio}}

{{#Definition}}<p>{{Definition}}</p>{{/Definition}}

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

.definition {
    background: #f2fbe7; 
    border: 1px solid #dff5c4; 
    border-radius: 6px; 
    color: #7a876b; 
    cursor: pointer;
}

.definition:hover {
    background: #dff5c4; 
    color: #000;
}

.definition .payload {
    display: none;
}

.definition.shown {
    background: #fff; 
    color: #000;
}

.definition.shown .payload {
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

result = create_anki_model(model_name, front_html, back_html, css)
print(result)
