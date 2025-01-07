from flask import Flask
from app.gui.heatmap import heatmap_bp
from app.gui.insights import insights_bp

def create_app():
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(heatmap_bp)
    app.register_blueprint(insights_bp)

    return app
