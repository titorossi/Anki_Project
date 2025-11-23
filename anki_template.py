import requests
import json

def create_anki_model(model_name):
    # The field names for the model
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
    <div  id="autoplay">{{Foreign phrase audio}}</div>

    <hr>
    
 <script>
 
 	var elem = document.querySelector("#autoplay .soundLink, #autoplay .replaybutton");
 	if (elem) {
 		elem.click();
 	}
 
 </script>
    """

    # Front and back for the receptive cards
    front_html_2 = """
    {{Foreign word}}<br>
    {{Foreign word audio}}

    <div class="line"></div>

		{{Foreign phrase}}<br>
		<div  id="autoplay">{{Foreign phrase audio}}</div>

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
    
 <script>
 
 	var elem = document.querySelector("#autoplay .soundLink, #autoplay .replaybutton");
 	if (elem) {
 		elem.click();
 	}
 
 </script>
    """
    back_html_2 = """
    {{Foreign word}}<br>
    {{Foreign word audio}}

    <div class="line"></div>

		{{Foreign phrase}}<br>
		{{Foreign phrase audio}}

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

    <hr id=answer>

    {{Native word}}<br>
    <div class="line"></div>
    {{Native phrase}}

    <hr>
    """

    css = """
    .card {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        font-size: 22px;
        text-align: center;
        color: #2c3e50;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 40px 20px;
        line-height: 1.6;
    }

    .line { 
        width: 60%; 
        max-width: 400px;
        margin: 20px auto; 
        border-top: 2px solid #3498db;
        opacity: 0.6;
    }

    hr {
        border: none;
        border-top: 1px solid rgba(0, 0, 0, 0.1);
        margin: 30px 0;
    }

    #answer {
        margin-top: 40px;
    }

    .toggle-content {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid #3498db;
        border-radius: 8px;
        color: #2980b9;
        cursor: pointer;
        margin: 20px auto;
        padding: 12px 20px;
        max-width: 500px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .toggle-content:hover {
        background: #3498db;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
    }

    .toggle-content .trigger {
        margin: 0;
        font-weight: 600;
        font-size: 16px;
    }

    .toggle-content .payload {
        display: none;
        margin-top: 10px;
        padding-top: 10px;
        border-top: 1px solid rgba(52, 152, 219, 0.3);
        font-size: 18px;
        line-height: 1.5;
    }

    .toggle-content.shown {
        background: white;
        color: #2c3e50;
        border-color: #2980b9;
    }

    .toggle-content.shown .payload {
        display: block;
        max-height: 200px;
        overflow-y: auto;
    }

    /* Audio buttons styling */
    .soundLink, .replaybutton {
        background: #3498db;
        border: none;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 2px 6px rgba(52, 152, 219, 0.3);
    }

    .soundLink:hover, .replaybutton:hover {
        background: #2980b9;
        transform: scale(1.1);
        box-shadow: 0 4px 10px rgba(52, 152, 219, 0.4);
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
