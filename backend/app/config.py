from pathlib import Path

from dotenv import load_dotenv
import os

_backend_dir = Path(__file__).resolve().parent.parent
load_dotenv(_backend_dir / ".env")

API_KEY = (os.getenv("WEATHER_API_KEY") or "").strip() or None
BASE_URL = "http://api.openweathermap.org/data/2.5"

WEATHER_CACHE_TTL = int(os.getenv("WEATHER_CACHE_TTL", "300"))
_cors = (os.getenv("CORS_ORIGINS") or "").strip()
CORS_ORIGINS = [o.strip() for o in _cors.split(",") if o.strip()] if _cors else []

RATE_LIMIT_WEATHER = os.getenv("RATE_LIMIT_WEATHER", "60 per minute").strip()
