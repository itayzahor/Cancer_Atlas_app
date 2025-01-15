from flask import Flask
from app.gui.heatmap import heatmap_bp
from app.gui.socioeconomic_analysis import socioeconomic_analysis_bp
from app.gui.risk_factors_analysis import risk_factors_analysis_bp
from app.gui.environmental_analysis import environmental_analysis_bp
from app.home import home_bp
from app.utilities import utilities_bp
import os
from flask_session import Session

def create_app():
    app = Flask(__name__)

    # Configure server-side session storage
    app.config['SESSION_TYPE'] = 'filesystem'  # Store sessions on the filesystem
    app.config['SESSION_FILE_DIR'] = './flask_session'  # Directory for session files
    app.config['SESSION_PERMANENT'] = False  # Session expires when the browser is closed
    app.config['SESSION_USE_SIGNER'] = True  # Sign session data for security
    app.secret_key = os.urandom(24)  # Ensure a secret key is set

    # Initialize Flask-Session
    Session(app)


    # Register Blueprints
    app.register_blueprint(utilities_bp, url_prefix='/utilities')
    app.register_blueprint(home_bp)
    app.register_blueprint(heatmap_bp, url_prefix='/heatmap')
    app.register_blueprint(socioeconomic_analysis_bp, url_prefix='/socioeconomic_analysis')
    app.register_blueprint(risk_factors_analysis_bp, url_prefix='/risk_factors_analysis')
    app.register_blueprint(environmental_analysis_bp, url_prefix='/environmental_analysis')

    return app
