This repository is a full-stack weather dashboard: a **Flask** backend talks to **OpenWeatherMap** for live conditions and daily-style forecasts, and a **Vue 3 + Vite + Tailwind** frontend lets you search by city, see current stats (temp, humidity, wind, and more), and browse up to six future days with labeled highs and lows and local SVG weather art. The stack also includes **server-side caching**, **rate limiting**, **structured logging**, **source attribution**, **unit preferences**, **recent cities**, and **optional geolocation** (coordinates go to the backend; your OWM key stays on the server).

# Weather forecast app

## Repository layout

```
weather_forecast/
├── backend/           # Flask API
└── weather-frontend/  # Vue 3 + Vite + Tailwind CSS
```

---

## Backend (`backend/`)

### Stack

- Python 3.x, Flask, flask-cors, Flask-Limiter, requests, python-dotenv

### Setup

1. Create and activate a virtual environment (from `backend/`):

   ```bash
   python -m venv venv
   ```

   Windows: `venv\Scripts\activate`  
   macOS/Linux: `source venv/bin/activate`

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy `backend/.env.example` to `backend/.env` and set at least:

   ```env
   WEATHER_API_KEY=your_openweathermap_api_key
   ```

   Do not commit `.env`. Optional variables are documented in `.env.example` (`WEATHER_CACHE_TTL`, `CORS_ORIGINS`, `RATE_LIMIT_WEATHER`, `LOG_LEVEL`, `SECRET_KEY`).

### Run

From `backend/`:

```bash
python run.py
```

Default URL: `http://127.0.0.1:5000`

### How the backend builds a response (matches the code)

1. **`GET /api/weather`** accepts either **`city`** (trimmed, non-empty) **or** **`lat` + `lon`** (floats in valid ranges). If `lat`/`lon` are partially sent or invalid, the API returns **400** with `{"error": "Invalid latitude or longitude"}`. If neither mode is satisfied, **400** with `{"error": "City is required, or provide lat and lon"}`.
2. **Cache** — The handler looks up an in-memory entry keyed by **`city:<lowercase city>`** or **`geo:<lat rounded 4dp>:<lon rounded 4dp>`**. If found and younger than **`WEATHER_CACHE_TTL`** (default 300 seconds), the handler returns the stored JSON immediately with **`meta.cache_hit`: true**. In that case **`meta.fetched_at`** is the **original** UTC time when that entry was first stored (not “now”).
3. **Upstream** — On a miss, it calls OpenWeatherMap **`/weather`** then **`/forecast`** (same query: city name or lat/lon). If the forecast call returns an error object without a `list`, the code still continues with an empty list (forecast can be rebuilt from Open-Meteo only).
4. **Assembly** — `format_weather` shapes **current** from OWM. **`build_six_day_forecast`** (in `formatter.py`) builds **six** local-calendar days **starting tomorrow** (today is excluded): it aggregates OWM’s 3-hour `list` by date using the location’s **`timezone`** offset, then **fills any missing dates** using [Open-Meteo](https://open-meteo.com/) daily data at **`raw_current["coord"]`** (no extra API key). WMO codes are mapped to OWM-like `condition` / `description` / `icon` for the frontend art.
5. **Success JSON** — The handler stores `{ fetched_at, current, forecast }` in the cache and returns it with **`meta`** (`sources`, `note`, `cache_hit: false`).
6. **Errors** — For upstream/config failures, responses are **`{"error": "..."}`** (and **`error_type`: `"config"`** is stripped before sending). These error bodies **do not** include `meta`, `current`, or `forecast`.
7. **Rate limiting** — **Flask-Limiter** applies **only** to **`GET /api/weather`** (not `/api/health` or `/api/test`). Default limit: **`60 per minute`** per client IP (`RATE_LIMIT_WEATHER`).

### API reference

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | JSON health payload (status, service name, UTC time). Not rate-limited. |
| GET | `/api/test` | Simple “backend working” message. Not rate-limited. |
| GET | `/api/weather?city=<name>` | Current + forecast. `city` required unless `lat`/`lon` are used. Rate-limited. |
| GET | `/api/weather?lat=<n>&lon=<n>` | Same as above using coordinates (browser geolocation flow). Rate-limited. |

**HTTP status summary**

| Status | When |
|--------|------|
| `200` | Success: `meta`, `current`, `forecast`. |
| `400` | Missing/invalid `city` or invalid `lat`/`lon`. |
| `404` | OWM could not resolve the city or coordinates. |
| `429` | Per-IP rate limit exceeded (`RATE_LIMIT_WEATHER`). |
| `503` | `WEATHER_API_KEY` missing or empty. |

**`meta` (success only)**

| Field | Meaning |
|--------|--------|
| `fetched_at` | ISO UTC timestamp when this cache entry was **first** stored (unchanged on cache hits). |
| `sources` | Static attribution: OpenWeatherMap + Open-Meteo with `id`, `label`, `url`, `role`. |
| `cache_hit` | `true` if served from TTL cache. |
| `note` | Fixed copy explaining six days from tomorrow and when Open-Meteo supplements OWM. |

**`current` fields** (always metric: °C, m/s)

`city`, `country`, `temperature`, `feels_like`, `humidity`, `condition`, `description`, `icon`, `wind_speed`.

**Each `forecast[]` item**

`date` (ISO date), `weekday`, `label`, `temp_min`, `temp_max`, `condition`, `description`, `icon`, `humidity`, `wind_speed`.

The frontend treats these numbers as **metric** and converts **only in the UI** when the user picks °F or mph.

**Success example (shape)**

```json
{
  "meta": {
    "fetched_at": "2026-03-23T12:00:00+00:00",
    "sources": [
      { "id": "openweathermap", "label": "OpenWeatherMap", "url": "https://openweathermap.org/", "role": "Current weather and 5-day / 3-hour forecast" },
      { "id": "open-meteo", "label": "Open-Meteo", "url": "https://open-meteo.com/", "role": "Daily values used to complete the 6-day outlook when needed" }
    ],
    "cache_hit": false,
    "note": "Six-day outlook starts tomorrow (today excluded). Open-Meteo may supply later days when the free OWM window ends."
  },
  "current": {
    "city": "…",
    "country": "…",
    "temperature": 0,
    "feels_like": 0,
    "humidity": 0,
    "condition": "…",
    "description": "…",
    "icon": "…",
    "wind_speed": 0
  },
  "forecast": [
    {
      "date": "YYYY-MM-DD",
      "weekday": "Mon",
      "label": "Mar 24",
      "temp_min": 0,
      "temp_max": 0,
      "condition": "…",
      "description": "…",
      "icon": "…",
      "humidity": 0,
      "wind_speed": 0
    }
  ]
}
```

### Structure

```
backend/
├── app/
│   ├── routes/weather_routes.py
│   ├── services/weather_service.py
│   ├── services/cache.py
│   ├── utils/formatter.py
│   ├── utils/open_meteo_daily.py
│   ├── extensions.py      # Flask-Limiter
│   ├── config.py
│   └── __init__.py
├── run.py
├── requirements.txt
├── .env.example
└── .env                   # you create this
```

---

## Frontend (`weather-frontend/`)

### Stack

- Vue 3, Vite, axios, Tailwind CSS

### Setup

From `weather-frontend/`:

```bash
npm install
```

Copy `weather-frontend/.env.example` to `.env` if you need a non-default API URL.

### Run

Development server:

```bash
npm run dev
```

Production build:

```bash
npm run build
npm run preview
```

Set `VITE_API_BASE_URL` (see `.env.example`) to point at your deployed API; default is `http://127.0.0.1:5000/api` (trailing slash is stripped in code).

### How the frontend uses the API (matches the code)

1. **`src/services/api.js`** — Axios instance with `baseURL` from `VITE_API_BASE_URL` or the localhost default. **`getWeather(city)`** → `GET /weather?city=…`. **`getWeatherByCoords(lat, lon)`** → `GET /weather?lat=…&lon=…`.
2. **`App.vue`** — Search submits **`getWeather`**; “Use my location” uses **`navigator.geolocation`** then **`getWeatherByCoords`**. On success it keeps **`bundle`** = full JSON (`meta`, `current`, `forecast`). **`addRecentCity`** runs after a successful city search or after geolocation when `current.city` exists (recent list in **`localStorage`** via `utils/recentCities.js`).
3. **Units** — API values stay metric; **`WeatherCard`** and **`ForecastSection`** use **`utils/displayUnits.js`** with preferences from **`utils/preferences.js`** (°C/°F, m/s/mph).
4. **Illustrations** — **`utils/weatherArt.js`** maps OWM-style `condition` / `icon` / `description` to SVGs under **`src/assets/weather/`**, rendered by **`WeatherIllustration.vue`**.
5. **Footer** — **`AppFooter.vue`** reads **`bundle.meta`** when present (last updated, cache hint, sources); before the first load it still shows the same source list and note from static defaults in that component.
6. **Errors** — Axios **`429`** shows a dedicated “too many requests” message; other failures use **`response.data.error`** when present. **`aria-live`** announces load/error status for assistive tech.

### Product features

- **Unit toggles** — °C / °F and m/s / mph (stored in `localStorage`).
- **Recent cities** — quick chips under the search field.
- **Use my location** — browser geolocation → `GET /api/weather?lat=&lon=`.
- **Attribution footer** — data sources, explanatory note, last updated time, cache hint.
- **Accessibility** — labeled search, `aria-live` status region, `aria-pressed` on unit toggles, landmark headings.

### Structure

```
weather-frontend/
├── src/
│   ├── components/     # App.vue, SearchBar, WeatherCard, ForecastSection, PreferencesBar, AppFooter, WeatherIllustration, …
│   ├── services/api.js
│   ├── utils/weatherArt.js
│   ├── utils/preferences.js
│   ├── utils/recentCities.js
│   ├── utils/displayUnits.js
│   ├── assets/weather/
│   ├── App.vue
│   ├── main.ts
│   └── style.css
├── vite.config.js
├── postcss.config.js
├── tailwind.config.js
├── .env.example
└── package.json
```

---

## Running both locally

1. Terminal A — `backend/`: activate venv, `python run.py`
2. Terminal B — `weather-frontend/`: `npm run dev`
3. Open the Vite URL (printed in the terminal, usually `http://localhost:5173`)

For stricter CORS in production, set `CORS_ORIGINS` on the backend to your frontend origin(s).

---

## Notes

- If Open-Meteo is unreachable, you may get fewer than six forecast cards; the UI notes when that happens.
- Keep API keys only in `backend/.env`. Set a strong `SECRET_KEY` in production.
- Rate limits and cache reduce load on OpenWeatherMap; tune `WEATHER_CACHE_TTL` and `RATE_LIMIT_WEATHER` as needed.
