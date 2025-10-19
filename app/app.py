
import app
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
import os
import io
import requests
import time
import secrets, string
from collections import Counter
import sys
import platform
from waitress import serve
sys.path.append("..")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
import write_a_new_pdf
# Configurações
UPLOAD_FOLDER = os.path.join(BASE_DIR, "../uploads")  # pasta para salvar arquivos YDK
ALLOWED_EXTENSIONS = {"ydk"}

# Cria pasta se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
print(BASE_DIR)

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
app.secret_key = ''.join(secrets.choice(alphabet) for _ in range(50))
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
                "genesys_points": card['misc_info'][0]['genesys_points'],
                "type" : card["type"]
            }
    return {"name": f"Unknown ({card_id})", "image_url": "", "quantity": 1, "genesys_points": 0}

@app.route("/", methods=["GET", "POST"])
def index():
    deck_data = {}
    loading = False
    submit_done = True
    decklistPath = ""
    decklist_ready = False


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

            for section, ids in sections.items():
                counter = Counter(ids)
                deck_data[section] = [
                    {**get_card_info(card_id), "quantity": qty} for card_id, qty in counter.items()
                ]
            submit_done = False
            decklist_ready = True
            
            dataUser = {
                "first_middle_names": request.form.get("first_middle_names", "").strip(),
                "last_names": request.form.get("last_names", "").strip(),
                "card_game_id": request.form.get("card_game_id", "").strip(),
                "event_date": request.form.get("event_date", "").strip(),
                "country_residency": request.form.get("country_residency", "").strip(),
                "event_name": request.form.get("event_name", "").strip(),
            }
            session["deck_data_user"] = dataUser
            session["decklist"] = deck_data
            
            decklistPath = write_a_new_pdf.fill_konami_decklist(dataUser, deck_data)
            
        else:
            flash("Invalid file type. Only .ydk allowed.")
            return redirect(request.url)
    return render_template("index.html", deck_data=deck_data, loading=loading, submit_done=submit_done,decklist_ready=decklist_ready)

# rota que serve o PDF (gera sob demanda)
@app.route("/decklist")
def decklist():
    dataUser = session.get("deck_data_user")
    decklist = session.get("decklist")
    if not dataUser:
        return "Nenhum PDF gerado ainda", 404

    # WriteANewPdf.fill_konami_decklist deve retornar bytes (como vc já tem)
    pdf_bytes = write_a_new_pdf.fill_konami_decklist(dataUser, decklist)
    return send_file(io.BytesIO(pdf_bytes),
                     mimetype="application/pdf",
                     as_attachment=False,
                     download_name="decklist.pdf")

if __name__ == "__main__":
    if platform.system() == "Windows":
        # On Windows, use the Flask development server
        app.run(debug=True, host="0.0.0.0", port=8080)
    else:
        # On Linux/macOS (ex: Railway)
        from waitress import serve
        serve(app, host="0.0.0.0", port=8080)
    
app = app