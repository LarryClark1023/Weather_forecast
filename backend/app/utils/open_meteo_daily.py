"""Map Open-Meteo daily rows to the same shape as our OpenWeatherMap daily summaries."""

from datetime import datetime


def wmo_code_to_owm_like(code: int) -> dict:
    """Approximate OWM `main` / description / icon for frontend illustrations."""
    if code == 0:
        return {"condition": "Clear", "description": "clear sky", "icon": "01d"}
    if code == 1:
        return {"condition": "Clouds", "description": "mainly clear", "icon": "02d"}
    if code == 2:
        return {"condition": "Clouds", "description": "partly cloudy", "icon": "03d"}
    if code == 3:
        return {"condition": "Clouds", "description": "overcast clouds", "icon": "04d"}
    if code in (45, 48):
        return {"condition": "Fog", "description": "fog", "icon": "50d"}
    if code in (51, 53, 55, 56, 57, 58, 59):
        return {"condition": "Drizzle", "description": "drizzle", "icon": "09d"}
    if code in (61, 63, 65, 66, 67, 68, 69, 80, 81, 82):
        return {"condition": "Rain", "description": "rain", "icon": "10d"}
    if code in (71, 73, 75, 77, 85, 86):
        return {"condition": "Snow", "description": "snow", "icon": "13d"}
    if code in (95, 96, 99):
        return {"condition": "Thunderstorm", "description": "thunderstorm", "icon": "11d"}
    return {"condition": "Clouds", "description": "cloudy", "icon": "03d"}


def open_meteo_daily_by_date(daily: dict) -> dict:
    """Return { 'YYYY-MM-DD': day_payload } matching our forecast card schema."""
    by_date = {}
    times = daily.get("time") or []
    codes = daily.get("weather_code") or []
    tmax = daily.get("temperature_2m_max") or []
    tmin = daily.get("temperature_2m_min") or []
    wmax = daily.get("wind_speed_10m_max") or []
    rh = daily.get("relative_humidity_2m_mean") or []

    for i, date_str in enumerate(times):
        if i >= len(codes):
            break
        d = datetime.fromisoformat(date_str).date()
        code_raw = codes[i]
        code = int(code_raw) if code_raw is not None else 3
        w = wmo_code_to_owm_like(code)
        t_hi = float(tmax[i]) if i < len(tmax) and tmax[i] is not None else 0.0
        t_lo = float(tmin[i]) if i < len(tmin) and tmin[i] is not None else 0.0
        wind = float(wmax[i]) if i < len(wmax) and wmax[i] is not None else 0.0
        hum = rh[i] if i < len(rh) and rh[i] is not None else 0
        by_date[d.isoformat()] = {
            "date": d.isoformat(),
            "weekday": d.strftime("%a"),
            "label": d.strftime("%b %d"),
            "temp_min": round(t_lo, 1),
            "temp_max": round(t_hi, 1),
            "condition": w["condition"],
            "description": w["description"],
            "icon": w["icon"],
            "humidity": int(round(hum)),
            "wind_speed": round(wind, 1),
        }
    return by_date
