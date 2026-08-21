from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})  # Tüm sayfalara ve isteklere izin verir

    # ... mevcut blueprint ve diğer ayarlarınız ...

    return app
