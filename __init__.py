from flask import Flask
import os

def create_app():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, "templates"),
        static_folder=os.path.join(BASE_DIR, "static")
    )

    # Importa rotas
    from . import routes
    app.register_blueprint(routes.bp)

    return app
