import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:5000/api',
});

export const getWeather = (city) => {
  return api.get('/weather', { params: { city } });
};
