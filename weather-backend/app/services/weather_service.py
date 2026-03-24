import requests

from app.config import API_KEY, BASE_URL

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


def get_current_weather(city):
    if not API_KEY:
        return {
            "error": "Weather API key is not configured. Set WEATHER_API_KEY in weather-backend/.env (or pass it into the container environment).",
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


def get_current_weather_coords(lat: float, lon: float):
    if not API_KEY:
        return {
            "error": "Weather API key is not configured. Set WEATHER_API_KEY in weather-backend/.env (or pass it into the container environment).",
            "error_type": "config",
        }

    response = requests.get(
        f"{BASE_URL}/weather",
        params={"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric"},
        timeout=15,
    )

    if response.status_code != 200:
        return {"error": "Location not found"}

    return response.json()


def get_forecast(city):
    if not API_KEY:
        return {
            "error": "Weather API key is not configured. Set WEATHER_API_KEY in weather-backend/.env (or pass it into the container environment).",
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


def get_forecast_coords(lat: float, lon: float):
    if not API_KEY:
        return {
            "error": "Weather API key is not configured. Set WEATHER_API_KEY in weather-backend/.env (or pass it into the container environment).",
            "error_type": "config",
        }

    response = requests.get(
        f"{BASE_URL}/forecast",
        params={"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric"},
        timeout=15,
    )

    if response.status_code != 200:
        return {"error": "Location not found"}

    return response.json()


def get_open_meteo_daily(lat: float, lon: float) -> dict | None:
    """
    Free daily forecast (no API key). Used to extend past OWM's ~5-day 3-hour horizon.
    """
    try:
        response = requests.get(
            OPEN_METEO_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "daily": (
                    "weather_code,temperature_2m_max,temperature_2m_min,"
                    "wind_speed_10m_max,relative_humidity_2m_mean"
                ),
                "forecast_days": 16,
                "timezone": "auto",
                "windspeed_unit": "ms",
            },
            timeout=15,
        )
        if response.status_code != 200:
            return None
        return response.json()
    except requests.RequestException:
        return None
