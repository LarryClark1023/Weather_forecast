from pathlib import Path

from dotenv import load_dotenv
import os

_backend_dir = Path(__file__).resolve().parent.parent
load_dotenv(_backend_dir / ".env")

API_KEY = (os.getenv("WEATHER_API_KEY") or "").strip() or None
BASE_URL = "http://api.openweathermap.org/data/2.5"
