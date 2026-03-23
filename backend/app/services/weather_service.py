import requests

from app.config import API_KEY, BASE_URL


def get_current_weather(city):
    if not API_KEY:
        return {
            "error": "Weather API key is not configured. Set WEATHER_API_KEY in backend/.env.",
            "error_type": "config",
        }

    response = requests.get(
        f"{BASE_URL}/weather",
        params={"q": city, "appid": API_KEY, "units": "metric"},
        timeout=15,
    )

    if response.status_code != 200:
        return {"error": "City not found"}

    return response.json()


def get_forecast(city):
    if not API_KEY:
        return {
            "error": "Weather API key is not configured. Set WEATHER_API_KEY in backend/.env.",
            "error_type": "config",
        }

    response = requests.get(
        f"{BASE_URL}/forecast",
        params={"q": city, "appid": API_KEY, "units": "metric"},
        timeout=15,
    )

    if response.status_code != 200:
        return {"error": "City not found"}

    return response.json()
