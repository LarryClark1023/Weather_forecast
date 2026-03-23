import logging
from datetime import datetime, timezone

from flask import Blueprint, jsonify, request

from app.config import RATE_LIMIT_WEATHER
from app.extensions import limiter
from app.services import cache as weather_cache
from app.services.weather_service import (
    get_current_weather,
    get_current_weather_coords,
    get_forecast,
    get_forecast_coords,
)
from app.utils.formatter import build_six_day_forecast, format_weather

logger = logging.getLogger(__name__)

weather_bp = Blueprint("weather", __name__)

DATA_SOURCES = [
    {
        "id": "openweathermap",
        "label": "OpenWeatherMap",
        "url": "https://openweathermap.org/",
        "role": "Current weather and 5-day / 3-hour forecast",
    },
    {
        "id": "open-meteo",
        "label": "Open-Meteo",
        "url": "https://open-meteo.com/",
        "role": "Daily values used to complete the 6-day outlook when needed",
    },
]


def _parse_coords():
    la = request.args.get("lat")
    lo = request.args.get("lon")
    if la is None or lo is None or la == "" or lo == "":
        return None
    try:
        lat_f = float(la)
        lon_f = float(lo)
    except (TypeError, ValueError):
        return "invalid"
    if not (-90.0 <= lat_f <= 90.0 and -180.0 <= lon_f <= 180.0):
        return "invalid"
    return (lat_f, lon_f)


def _cache_key_city(city: str) -> str:
    return f"city:{city.strip().lower()}"


def _cache_key_coords(lat: float, lon: float) -> str:
    return f"geo:{round(lat, 4)}:{round(lon, 4)}"


def _assemble_body(raw_current: dict, raw_forecast: dict) -> dict:
    if "error" in raw_forecast and "list" not in raw_forecast:
        raw_forecast = {"list": []}
    forecast_days = build_six_day_forecast(raw_current, raw_forecast)
    return {
        "current": format_weather(raw_current),
        "forecast": forecast_days,
    }


@weather_bp.route("/weather")
@limiter.limit(RATE_LIMIT_WEATHER)
def weather():
    coords = _parse_coords()
    if coords == "invalid":
        return jsonify({"error": "Invalid latitude or longitude"}), 400

    if coords is not None:
        lat_f, lon_f = coords
        cache_key = _cache_key_coords(lat_f, lon_f)
        log_label = f"lat={lat_f} lon={lon_f}"
    else:
        city = (request.args.get("city") or "").strip()
        if not city:
            return jsonify({"error": "City is required, or provide lat and lon"}), 400
        cache_key = _cache_key_city(city)
        log_label = f"city={city!r}"

    cached = weather_cache.get(cache_key)
    if cached is not None:
        logger.info("weather cache hit %s", log_label)
        return jsonify(
            {
                "meta": {
                    "fetched_at": cached["fetched_at"],
                    "sources": DATA_SOURCES,
                    "cache_hit": True,
                    "note": (
                        "Six-day outlook starts tomorrow (today excluded). "
                        "Open-Meteo may supply later days when the free OWM window ends."
                    ),
                },
                "current": cached["current"],
                "forecast": cached["forecast"],
            }
        )

    if coords is not None:
        lat_f, lon_f = coords
        raw_current = get_current_weather_coords(lat_f, lon_f)
    else:
        raw_current = get_current_weather(city)

    if "error" in raw_current:
        status = 503 if raw_current.get("error_type") == "config" else 404
        payload = {k: v for k, v in raw_current.items() if k != "error_type"}
        logger.info("weather upstream error %s status=%s", log_label, status)
        return jsonify(payload), status

    if coords is not None:
        lat_f, lon_f = coords
        raw_forecast = get_forecast_coords(lat_f, lon_f)
    else:
        raw_forecast = get_forecast(city)

    body = _assemble_body(raw_current, raw_forecast)
    fetched_at = datetime.now(timezone.utc).isoformat()
    to_cache = {"fetched_at": fetched_at, **body}
    weather_cache.set(cache_key, to_cache)

    logger.info("weather fetched %s", log_label)

    return jsonify(
        {
            "meta": {
                "fetched_at": fetched_at,
                "sources": DATA_SOURCES,
                "cache_hit": False,
                "note": (
                    "Six-day outlook starts tomorrow (today excluded). "
                    "Open-Meteo may supply later days when the free OWM window ends."
                ),
            },
            **body,
        }
    )


@weather_bp.route("/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "service": "weather-backend",
            "time": datetime.now(timezone.utc).isoformat(),
        }
    )


@weather_bp.route("/test")
def test():
    return jsonify({"message": "Backend is working!"})
