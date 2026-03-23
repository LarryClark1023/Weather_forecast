import axios from 'axios';

const baseURL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, '') || 'http://127.0.0.1:5000/api';

const api = axios.create({ baseURL });

export const getWeather = (city) => api.get('/weather', { params: { city } });

export const getWeatherByCoords = (lat, lon) =>
  api.get('/weather', { params: { lat, lon } });
