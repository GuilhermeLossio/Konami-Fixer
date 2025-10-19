# <div align="center" style="margin-bottom: 20px;">
  <a href="https://github.com/GuilhermeLossio/Konami-Fixer/blob/main/app/static/BabyNoodle.png" target="_blank" rel="noopener">
    <img src="./app/static/BabyNoodle.png" alt="BabyNoodle logo" width="90">
  </a>

  <h1>Konami-Fixer / DiNoodle</h1>

  <p>
    <strong>by <a href="https://github.com/GuilhermeLossio">@GuilhermeLossio</a></strong><br>
    A small tool to validate, fix and generate tournament-style decklists for Konami's official format (.ydk).
  </p>

  <p>
    <a href="https://dinoodle.up.railway.app/">🚀 Live Demo</a>
  </p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.8%2B-blue" alt="Python">
    <img src="https://img.shields.io/badge/Flask-2.x-green" alt="Flask">
    <img src="https://img.shields.io/badge/License-MIT-blue" alt="License">
    <img src="https://img.shields.io/badge/Status-Active-success" alt="Status">
  </p>
</div>

---

## Overview

DiNoodle is a lightweight utility that:
- Parses and fixes .ydk deck files
- Validates card names and IDs using the YGOPRODeck API
- Generates a printable PDF decklist formatted to match Konami's official tournament style

The project includes a web UI for manual edits, helper scripts for automation, and an optional Flask API for integrations with tournament tools.

---

## Features

- Upload and automatically fix .ydk deck files
- Normalize card names and map to official IDs from YGOPRODeck
- Generate tournament-style PDF decklists ready to print
- Web UI to edit player and event information
- Helper scripts for batch processing (Python, PowerShell, Batch)
- Optional Flask endpoints for automation

---

## Demo

Live deployment: https://dinoodle.up.railway.app/

---

## Tech Stack

- Backend: Python (Flask)
- External API: YGOPRODeck
- Frontend: HTML, CSS, JavaScript
- Automation: PowerShell / Batch / Python scripts
- Deployment: Railway

---

## Requirements

- Python 3.8+
- pip
- A modern browser (for the web UI)
- (Optional) Node.js / npm — only if you add frontend build tooling

---

## Quick Start (Local)

1. Clone the repository
   ```
   git clone https://github.com/GuilhermeLossio/Konami-Fixer.git
   cd Konami-Fixer
   ```

2. Create and activate a virtual environment
   - macOS / Linux
     ```
     python -m venv .venv
     source .venv/bin/activate
     ```
   - Windows (PowerShell)
     ```
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Recommended environment variables (use a .env file or platform settings)
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   YGOPRO_API_BASE=https://db.ygoprodeck.com/api/v7/
   SECRET_KEY=your_secret_key_here
   ```

5. Run the app
   ```
   # Option 1 (Flask)
   flask run --host=0.0.0.0 --port=5000

   # Option 2 (direct)
   python app.py
   ```

6. Open: http://localhost:5000

---

## Project Structure

```
Konami-Fixer/
├── app.py / run.py         # Flask entrypoint
├── requirements.txt        # Python dependencies
├── templates/              # Jinja2 HTML templates
├── app/static/             # Static assets (css, js, images)
│   └── BabyNoodle.png
├── scripts/                # Helper scripts (.ps1, .bat, .py)
└── docs/                   # Additional documentation
```

---

## Usage

1. Open the web UI.
2. Upload a .ydk deck file.
3. Review suggested fixes (name normalization, ID mapping, card counts).
4. Edit player/event details if needed.
5. Export the verified decklist as a PDF ready for printing.

Batch processing: use the scripts in `scripts/` to process multiple .ydk files automatically.

---

## API / Integration Notes

- The app queries the public YGOPRODeck API by default. Change `YGOPRO_API_BASE` if you need a different endpoint.
- A simple Flask API is included for programmatic corrections—check the `app` package (routes) to see available endpoints and expected payloads.

---

## Customization & Printing

- PDF layout and decklist templates are in `templates/`. Edit them to change the layout, add localization, or adjust print settings.

---

## Development & Contribution

Contributions are welcome:
- Open an issue for bugs, feature requests or questions.
- Fork the repo, create a branch for your feature/fix, add tests, and open a PR.
- Keep changes small and document behavior in the README or docs.

---

## Roadmap

Planned improvements:
- Export decklists in JSON
- Dark mode for the UI
- Banlist/forbidden list validation by date
- CLI for batch processing
- Better i18n support for PDFs

---

## License

MIT — see LICENSE for full details.

---

## Contact

Maintainer: @GuilhermeLossio  
Email: guilhermelossio@gmail.com  
Live App: https://dinoodle.up.railway.app/
