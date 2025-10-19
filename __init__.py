from flask import Flask
import os

def create_app():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, "templates"),
        static_folder=os.path.join(BASE_DIR, "static")
    )

    # Importa o app.py como módulo do pacote
    from . import app as app_module

    return app
