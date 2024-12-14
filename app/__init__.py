from flask import Flask
from flask_cors import CORS
from config import Config

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    from app.routes import api_bp
    app.register_blueprint(api_bp)
    
    return app