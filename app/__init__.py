from flask import Flask
from flask_cors import CORS
from .routes import main

def create_app():
    app = Flask(__name__)
    
    # Tüm domainlerden gelen isteklere (Wix dahil) izin ver
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Rotaları uygulamaya kaydet
    app.register_blueprint(main)
    
    return app
