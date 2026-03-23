from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    from app.routes.weather_routes import weather_bp
    app.register_blueprint(weather_bp, url_prefix="/api")

    return app