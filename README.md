<div align="center" style="margin-bottom: 20px;">
  <a href="https://github.com/GuilhermeLossio/Konami-Fixer/blob/main/app/static/BabyNoodle.png" target="_blank" rel="noopener">
    <img src="./app/static/BabyNoodle.png" alt="BabyNoodle logo" width="90">
  </a>

  <h1>Konami-Fixer / DiNoodle</h1>

  <p>
    <b>by <a href="https://github.com/GuilhermeLossio">@GuilhermeLossio</a></b>  
    Tool to fix and generate tournament decklists for Konami's official format.
  </p>

  <p>
    <a href="https://dinoodle.up.railway.app/">🚀 Live Demo</a>
  </p>

  <!-- Badges -->
  <p>
    <img src="https://img.shields.io/badge/Python-3.8+-blue" alt="Python">
    <img src="https://img.shields.io/badge/Flask-2.x-green" alt="Flask">
    <img src="https://img.shields.io/badge/License-MIT-blue" alt="License">
    <img src="https://img.shields.io/badge/Status-Active-success" alt="Status">
  </p>
</div>

---

## 🧩 Overview

**DiNoodle** is a lightweight tool that parses and fixes `.ydk` deck files, validating cards using the **Ygoprodeck API** and generating a **printable PDF decklist** that follows Konami’s official format.  
It includes a web UI, helper scripts, and an optional Flask API for automation or integration with tournament tools.

---

## ⚡ Quick Start

```bash
git clone https://github.com/GuilhermeLossio/Konami-Fixer.git
cd Konami-Fixer
pip install -r requirements.txt
python app.py
Then open http://localhost:5000 in your browser.

📋 Table of Contents
Features

Demo

Tech Stack

Requirements

Installation (local)

Environment Variables

Running Locally

Deployment (Railway)

Project Layout

Roadmap / Future Plans

License

Contact

✨ Features
✅ Upload .ydk deck files

🔍 Validate and normalize cards using Ygoprodeck API

🧾 Generate official-style printable PDF decklists

🧑‍💻 Web UI for player and event info

🪄 Helper scripts for Python, PowerShell, and Batch

🎮 Demo
Live deployment: https://dinoodle.up.railway.app/

<br> <img src="./app/static/BabyNoodle.png" alt="Screenshot" width="400">
🧠 Tech Stack
Backend: Python + Flask

External API: Ygoprodeck

Frontend: HTML, CSS, JavaScript

Automation: PowerShell, Batch

Deployment: Railway

🧰 Requirements
Python 3.8+

pip

A modern browser for the UI

(Optional) Node.js / npm if frontend build steps are added

⚙️ Installation (local)
Clone the repository:

bash
Copiar código
git clone https://github.com/GuilhermeLossio/Konami-Fixer.git
cd Konami-Fixer
Create and activate a virtual environment:

bash
Copiar código
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
Install dependencies:

bash
Copiar código
pip install -r requirements.txt
If missing, install the basics manually:

bash
Copiar código
pip install flask requests python-dotenv
🔐 Environment Variables
Recommended variables (set in your system or .env file):

bash
Copiar código
FLASK_APP=app.py
FLASK_ENV=development
YGOPRO_API_BASE=https://db.ygoprodeck.com/api/v7/
SECRET_KEY=some_secure_value
If deploying on Railway, configure these in the Railway dashboard.

🏃 Running Locally
Activate the virtual environment.

Ensure environment variables are set.

Start the app:

bash
Copiar código
flask run --host=0.0.0.0 --port=5000
# or
python app.py
Then open http://localhost:5000.

☁️ Deployment (Railway)
The project is already deployed at:
https://dinoodle.up.railway.app/

Add environment variables on the Railway dashboard (YGOPRO_API_BASE, SECRET_KEY, etc.).

Ensure your entrypoint (Procfile or settings) runs the Flask app.

📂 Project Layout
bash
Copiar código
Konami-Fixer/
├── app.py / run.py         # Flask entrypoint
├── requirements.txt         # Python dependencies
├── templates/               # Jinja2 HTML templates
├── app/static/              # Static assets (css, js, images)
│   └── BabyNoodle.png       # Project logo
├── scripts/                 # Helper scripts (.ps1, .bat, .py)
└── docs/                    # Additional documentation
🧭 Roadmap / Future Plans
 Export decklists in JSON format

 Add dark mode UI

 Validate tournament legality by date

 Add CLI version for batch deck fixes

 Enhance PDF generator for localization support

📜 License
This project is licensed under the MIT License — see the LICENSE file for details.

💬 Contact
Maintainer: @GuilhermeLossio

Email: guilhermelossio@gmail.com

Live App: https://dinoodle.up.railway.app/

yaml
Copiar código

---

Se quiser, posso também gerar um **LICENSE.md** pronto com o texto completo do MIT (com seu nome e ano).  
Quer que eu inclua isso também?






Você disse:
Está saindo no chat. Pode fazer ele vir como texto?


O ChatGPT disse:
Perfeito 😄 aqui está o conteúdo do README como texto puro, pronto para você copiar e colar no seu repositório (sem blocos de código do chat):

<div align="center" style="margin-bottom: 20px;"> <a href="https://github.com/GuilhermeLossio/Konami-Fixer/blob/main/app/static/BabyNoodle.png" target="_blank" rel="noopener"> <img src="./app/static/BabyNoodle.png" alt="BabyNoodle logo" width="90"> </a> <h1>Konami-Fixer / DiNoodle</h1> <p> <b>by <a href="https://github.com/GuilhermeLossio">@GuilhermeLossio</a></b> Tool to fix and generate tournament decklists for Konami's official format. </p> <p> <a href="https://dinoodle.up.railway.app/">🚀 Live Demo</a> </p> <!-- Badges --> <p> <img src="https://img.shields.io/badge/Python-3.8+-blue" alt="Python"> <img src="https://img.shields.io/badge/Flask-2.x-green" alt="Flask"> <img src="https://img.shields.io/badge/License-MIT-blue" alt="License"> <img src="https://img.shields.io/badge/Status-Active-success" alt="Status"> </p> </div>
🧩 Overview
Konami-Fixer / DiNoodle is a lightweight tool that parses and fixes .ydk deck files, validating cards using the Ygoprodeck API and generating a printable PDF decklist that follows Konami’s official format.
It includes a web UI, helper scripts, and an optional Flask API for automation or integration with tournament tools.

⚡ Quick Start
bash
Copiar código
git clone https://github.com/GuilhermeLossio/Konami-Fixer.git
cd Konami-Fixer
pip install -r requirements.txt
python app.py
Then open http://localhost:5000 in your browser.

📋 Table of Contents
Features

Demo

Tech Stack

Requirements

Installation (local)

Environment Variables

Running Locally

Deployment (Railway)

Project Layout

Roadmap / Future Plans

License

Contact

✨ Features
✅ Upload .ydk deck files

🔍 Validate and normalize cards using Ygoprodeck API

🧾 Generate official-style printable PDF decklists

🧑‍💻 Web UI for player and event info

🪄 Helper scripts for Python, PowerShell, and Batch

🎮 Demo
Live deployment: https://dinoodle.up.railway.app/

<br> <img src="./app/static/BabyNoodle.png" alt="Screenshot" width="400">
🧠 Tech Stack
Backend: Python + Flask

External API: Ygoprodeck

Frontend: HTML, CSS, JavaScript

Automation: PowerShell, Batch

Deployment: Railway

🧰 Requirements
Python 3.8+

pip

A modern browser for the UI

(Optional) Node.js / npm if frontend build steps are added

⚙️ Installation (local)
Clone the repository:

bash
Copiar código
git clone https://github.com/GuilhermeLossio/Konami-Fixer.git
cd Konami-Fixer
Create and activate a virtual environment:

bash
Copiar código
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
Install dependencies:

bash
Copiar código
pip install -r requirements.txt
If missing, install the basics manually:

bash
Copiar código
pip install flask requests python-dotenv
🔐 Environment Variables
Recommended variables (set in your system or .env file):

bash
Copiar código
FLASK_APP=app.py
FLASK_ENV=development
YGOPRO_API_BASE=https://db.ygoprodeck.com/api/v7/
SECRET_KEY=some_secure_value
If deploying on Railway, configure these in the Railway dashboard.

🏃 Running Locally
Activate the virtual environment.

Ensure environment variables are set.

Start the app:

bash
Copiar código
flask run --host=0.0.0.0 --port=5000
# or
python app.py
Then open http://localhost:5000.

☁️ Deployment (Railway)
The project is already deployed at:
https://dinoodle.up.railway.app/

Add environment variables on the Railway dashboard (YGOPRO_API_BASE, SECRET_KEY, etc.).

Ensure your entrypoint (Procfile or settings) runs the Flask app.

📂 Project Layout
bash
Copiar código
Konami-Fixer/
├── app.py / run.py         # Flask entrypoint
├── requirements.txt         # Python dependencies
├── templates/               # Jinja2 HTML templates
├── app/static/              # Static assets (css, js, images)
│   └── BabyNoodle.png       # Project logo
├── scripts/                 # Helper scripts (.ps1, .bat, .py)
└── docs/                    # Additional documentation
🧭 Roadmap / Future Plans
 Export decklists in JSON format

 Add dark mode UI

 Validate tournament legality by date

 Add CLI version for batch deck fixes

 Enhance PDF generator for localization support

📜 License
This project is licensed under the MIT License — see the LICENSE file for details.

💬 Contact
Maintainer: @GuilhermeLossio

Email: guilhermelossio@gmail.com

Live App: https://dinoodle.up.railway.app/

Se quiser, posso agora gerar o conteúdo do arquivo LICENSE (MIT) já preenchido com seu nome e o ano atual — quer que eu envie também?
