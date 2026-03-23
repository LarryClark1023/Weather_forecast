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

### API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | JSON health payload (status, service name, UTC time). |
| GET | `/api/test` | Simple “backend working” message. |
| GET | `/api/weather?city=<name>` | Current + forecast. `city` required unless `lat`/`lon` are used. |
| GET | `/api/weather?lat=<n>&lon=<n>` | Same as above using coordinates (browser geolocation flow). |

**Responses**

- `200` — body includes `meta`, `current`, and `forecast`.
- `400` — missing/invalid input.
- `404` — city or coordinates not found upstream.
- `429` — too many requests (rate limit; see `RATE_LIMIT_WEATHER`).
- `503` — missing `WEATHER_API_KEY`.

`meta` includes:

- `fetched_at` — ISO UTC timestamp when data was loaded from upstream (or from cache).
- `sources` — attribution list (OpenWeatherMap, Open-Meteo) with URLs and short roles.
- `cache_hit` — whether the payload was served from the in-memory TTL cache.
- `note` — short explanation of the six-day window and provider mix.

Numeric fields in `current` / `forecast` are **metric** (°C, m/s); the frontend converts for display when the user chooses °F or mph.

Success shape (abbreviated):

```json
{
  "meta": {
    "fetched_at": "2026-03-23T12:00:00+00:00",
    "sources": [ { "id": "openweathermap", "label": "...", "url": "...", "role": "..." } ],
    "cache_hit": false,
    "note": "..."
  },
  "current": { "city": "...", "temperature": 0, "wind_speed": 0, "..." : "..." },
  "forecast": [ { "date": "YYYY-MM-DD", "temp_min": 0, "temp_max": 0, "..." : "..." } ]
}
```

The six-day outlook (starting tomorrow) uses OpenWeatherMap’s 3-hour forecast when possible; any missing calendar days are filled using [Open-Meteo](https://open-meteo.com/) at the same coordinates (no extra API key).

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

Set `VITE_API_BASE_URL` (see `.env.example`) to point at your deployed API; default is `http://127.0.0.1:5000/api`.

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
│   ├── components/
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
