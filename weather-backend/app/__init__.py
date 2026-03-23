import logging
import os

from flask import Flask
from flask_cors import CORS

from app.config import CORS_ORIGINS, WEATHER_CACHE_TTL
from app.extensions import limiter
from app.services import cache as weather_cache


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-only-change-in-production")
    app.config["WEATHER_CACHE_TTL"] = WEATHER_CACHE_TTL

    if CORS_ORIGINS:
        CORS(
            app,
            resources={r"/api/*": {"origins": CORS_ORIGINS}},
            supports_credentials=True,
        )
    else:
        CORS(app)

    weather_cache.configure(WEATHER_CACHE_TTL)

    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    limiter.init_app(app)

    from app.routes.weather_routes import weather_bp

    app.register_blueprint(weather_bp, url_prefix="/api")

    return app
