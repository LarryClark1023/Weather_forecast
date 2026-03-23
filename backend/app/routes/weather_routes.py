from flask import Blueprint, request, jsonify

from app.services.weather_service import get_current_weather, get_forecast
from app.utils.formatter import format_daily_forecast, format_weather

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
    forecast_days = []
    if "list" in raw_forecast:
        forecast_days = format_daily_forecast(raw_forecast, num_days=6)

    return jsonify(
        {
            "current": format_weather(raw_current),
            "forecast": forecast_days,
        }
    )


@weather_bp.route("/test")
def test():
    return jsonify({"message": "Backend is working!"})
