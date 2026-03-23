from flask import Blueprint, request, jsonify

from app.services.weather_service import get_current_weather, get_forecast
from app.utils.formatter import build_six_day_forecast, format_weather

weather_bp = Blueprint("weather", __name__)


@weather_bp.route("/weather")
def weather():
    city = (request.args.get("city") or "").strip()
    if not city:
        return jsonify({"error": "City is required"}), 400

    raw_current = get_current_weather(city)
    if "error" in raw_current:
        status = 503 if raw_current.get("error_type") == "config" else 404
        payload = {k: v for k, v in raw_current.items() if k != "error_type"}
        return jsonify(payload), status

    raw_forecast = get_forecast(city)
    if "error" in raw_forecast and "list" not in raw_forecast:
        raw_forecast = {"list": []}

    forecast_days = build_six_day_forecast(raw_current, raw_forecast)

    return jsonify(
        {
            "current": format_weather(raw_current),
            "forecast": forecast_days,
        }
    )


@weather_bp.route("/test")
def test():
    return jsonify({"message": "Backend is working!"})
