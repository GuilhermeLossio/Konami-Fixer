from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import requests
import time
from collections import Counter

# Configurações
UPLOAD_FOLDER = "../src/uploads"  # pasta para salvar arquivos YDK
ALLOWED_EXTENSIONS = {"ydk"}

# Cria pasta se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(
    __name__,
    template_folder="../src/templates",
    static_folder="../src/static"
)
app.secret_key = "supersecretkey"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Função para validar extensão
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Função para ler YDK
def parse_ydk(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    sections = {"main": [], "extra": [], "side": []}
    current_section = "main"

    for line in lines:
        line = line.strip()
        if line == "#main":
            current_section = "main"
        elif line == "#extra":
            current_section = "extra"
        elif line == "!side":
            current_section = "side"
        elif line.startswith("#") or line == "":
            continue
        else:
            sections[current_section].append(line)
    return sections

# Função para buscar info da carta via API YGOPRODeck
def get_card_info(card_id):
    url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
    params = {
        "id": card_id,
        "misc": "yes",
        "format" : "genesys"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json().get("data", [])
        if data:
            card = data[0]
            genesysPoints = card.get('genesys_points', 0)
            return {
                "name": card["name"],
                "image_url": card["card_images"][0]["image_url"],
                "quantity": 1,
                "genesys_points": card['misc_info'][0]['genesys_points']
            }
    return {"name": f"Unknown ({card_id})", "image_url": "", "quantity": 1, "genesys_points": 0}

@app.route("/", methods=["GET", "POST"])
def index():
    deck_data = None
    loading = False
    submit_done = True

    if request.method == "POST":
        if "deckFile" not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files["deckFile"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(file_path)

            loading = True
            time.sleep(1)  # apenas efeito de loading
            ##session['submit_done'] = False

            sections = parse_ydk(file_path)

            # Contar repetições e gerar deck_data
            deck_data = {}
            for section, ids in sections.items():
                counter = Counter(ids)
                deck_data[section] = [
                    {**get_card_info(card_id), "quantity": qty} for card_id, qty in counter.items()
                ]
            submit_done = False
        else:
            flash("Invalid file type. Only .ydk allowed.")
            return redirect(request.url)
    return render_template("index.html", deck_data=deck_data, loading=loading, submit_done=submit_done)

if __name__ == "__main__":
    app.run(debug=True)
