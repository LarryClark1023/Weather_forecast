This repository is a full-stack weather dashboard: a **Flask** backend talks to **OpenWeatherMap** for live conditions and daily-style forecasts, and a **Vue 3 + Vite + Tailwind** frontend lets you search by city, see current stats (temp, humidity, wind, and more), and browse up to six future days with labeled highs and lows and local SVG weather art.

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

- Python 3.x, Flask, flask-cors, requests, python-dotenv

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

3. Create `backend/.env` (same folder as `run.py`):

   ```env
   WEATHER_API_KEY=your_openweathermap_api_key
   ```

   Do not commit `.env`.

### Run

From `backend/`:

```bash
python run.py
```

Default URL: `http://127.0.0.1:5000`

### API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/test` | Health check |
| GET | `/api/weather?city=<name>` | Current weather + daily forecast (tomorrow onward, up to 6 days). `city` is required (trimmed). |

Success body shape:

```json
{
  "current": {
    "city": "...",
    "country": "...",
    "temperature": 0,
    "feels_like": 0,
    "humidity": 0,
    "condition": "...",
    "description": "...",
    "icon": "...",
    "wind_speed": 0
  },
  "forecast": [
    {
      "date": "YYYY-MM-DD",
      "weekday": "Mon",
      "label": "Mar 23",
      "temp_min": 0,
      "temp_max": 0,
      "condition": "...",
      "description": "...",
      "icon": "...",
      "humidity": 0,
      "wind_speed": 0
    }
  ]
}
```

Errors: `400` (missing city), `404` (city not found), `503` (missing `WEATHER_API_KEY`).

### Structure

```
backend/
├── app/
│   ├── routes/weather_routes.py
│   ├── services/weather_service.py
│   ├── utils/formatter.py
│   ├── config.py
│   └── __init__.py
├── run.py
├── requirements.txt
└── .env          # you create this
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

The app calls the API at `http://127.0.0.1:5000/api`. Start the backend first, or change the base URL in `src/services/api.js` if you deploy elsewhere.

### Structure

```
weather-frontend/
├── src/
│   ├── components/
│   ├── services/api.js
│   ├── assets/weather/    # condition SVG illustrations
│   ├── utils/weatherArt.js
│   ├── App.vue
│   ├── main.ts
│   └── style.css
├── vite.config.js
├── postcss.config.js
├── tailwind.config.js
└── package.json
```

---

## Running both locally

1. Terminal A — `backend/`: activate venv, `python run.py`
2. Terminal B — `weather-frontend/`: `npm run dev`
3. Open the Vite URL (printed in the terminal, usually `http://localhost:5173`)

---

## Notes

- OpenWeatherMap **free** forecast data may return fewer than six future days; the UI explains when that happens.
- Keep API keys only in `backend/.env`.
