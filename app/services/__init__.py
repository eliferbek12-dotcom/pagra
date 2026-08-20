from flask import Flask
from flask_cors import CORS
from .routes import main

def create_app():
    app = Flask(__name__)
    
    # Tüm route'lara dışarıdan (Wix dahil) erişim izni ver:
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    app.register_blueprint(main)
    
    return app