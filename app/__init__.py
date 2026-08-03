from flask import Flask
from flask_cors import CORS
from .routes import main

def create_app():
    app = Flask(__name__)

    # Güvenli CORS: sadece belirli sitelere izin ver
    CORS(app, origins=[
        "http://localhost:3000",   # geliştirme ortamı
        "https://senin-siten.com"  # prod ortamı (gerçek domain buraya gelecek)
    ])

    app.register_blueprint(main)
    return app

