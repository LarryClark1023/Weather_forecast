from collections import defaultdict
from datetime import datetime, timedelta, timezone


def format_weather(data):
    return {
        "city": data["name"],
        "country": data.get("sys", {}).get("country"),
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "condition": data["weather"][0]["main"],
        "description": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"],
        "wind_speed": data.get("wind", {}).get("speed", 0),
    }


def _local_datetime(unix_ts: int, tz_offset_sec: int) -> datetime:
    utc = datetime.fromtimestamp(unix_ts, tz=timezone.utc)
    return utc + timedelta(seconds=tz_offset_sec)


def format_daily_forecast(data, num_days: int = 6):
    """
    Build up to `num_days` daily summaries starting tomorrow (city-local dates),
    excluding today. The free OWM 3-hour feed may not cover all `num_days`;
    `build_six_day_forecast` fills gaps with Open-Meteo.
    """
    tz_off = data["city"]["timezone"]
    now_local_date = (_local_datetime(int(datetime.now(timezone.utc).timestamp()), tz_off)).date()
    start_date = now_local_date + timedelta(days=1)

    by_date = defaultdict(list)
    for item in data.get("list", []):
        d = _local_datetime(item["dt"], tz_off).date()
        if d >= start_date:
            by_date[d].append(item)

    sorted_dates = sorted(by_date.keys())[:num_days]
    days = []

    for d in sorted_dates:
        slots = by_date[d]
        temp_mins = [s["main"].get("temp_min", s["main"]["temp"]) for s in slots]
        temp_maxs = [s["main"].get("temp_max", s["main"]["temp"]) for s in slots]
        hums = [s["main"]["humidity"] for s in slots]
        winds = [s.get("wind", {}).get("speed", 0) for s in slots]

        noon_slot = min(
            slots,
            key=lambda s: abs(_local_datetime(s["dt"], tz_off).hour - 12),
        )
        w0 = noon_slot["weather"][0]

        days.append(
            {
                "date": d.isoformat(),
                "weekday": d.strftime("%a"),
                "label": d.strftime("%b %d"),
                "temp_min": round(min(temp_mins), 1),
                "temp_max": round(max(temp_maxs), 1),
                "condition": w0["main"],
                "description": w0["description"],
                "icon": w0["icon"],
                "humidity": int(round(sum(hums) / len(hums))),
                "wind_speed": round(max(winds), 1),
            }
        )

    return days


def build_six_day_forecast(raw_current: dict, raw_forecast: dict) -> list:
    """
    Six calendar days starting tomorrow (city-local), excluding today.
    Prefer OpenWeatherMap 3-hour aggregation; fill gaps with Open-Meteo daily (free, no key)
    so the sixth day appears when OWM's 5-day window runs out.
    """
    from app.services.weather_service import get_open_meteo_daily
    from app.utils.open_meteo_daily import open_meteo_daily_by_date

    num_days = 6
    tz_off = raw_current["timezone"]
    now_local_date = (
        _local_datetime(int(datetime.now(timezone.utc).timestamp()), tz_off)
    ).date()
    target_dates = [now_local_date + timedelta(days=i + 1) for i in range(num_days)]

    owm_days = (
        format_daily_forecast(raw_forecast, num_days=num_days)
        if raw_forecast.get("list")
        else []
    )
    by_owm = {d["date"]: d for d in owm_days}

    need_fill = any(td.isoformat() not in by_owm for td in target_dates)
    om_by_date = {}
    if need_fill:
        coord = raw_current.get("coord") or {}
        lat, lon = coord.get("lat"), coord.get("lon")
        if lat is not None and lon is not None:
            om = get_open_meteo_daily(float(lat), float(lon))
            if om and om.get("daily"):
                om_by_date = open_meteo_daily_by_date(om["daily"])

    out = []
    for td in target_dates:
        key = td.isoformat()
        if key in by_owm:
            out.append(by_owm[key])
        elif key in om_by_date:
            out.append(om_by_date[key])
    return out
