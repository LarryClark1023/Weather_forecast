import sunny from '../assets/weather/sunny.svg?url';
import nightClear from '../assets/weather/night-clear.svg?url';
import partlyCloudy from '../assets/weather/partly-cloudy.svg?url';
import cloudy from '../assets/weather/cloudy.svg?url';
import rainy from '../assets/weather/rainy.svg?url';
import storm from '../assets/weather/storm.svg?url';
import snow from '../assets/weather/snow.svg?url';
import fog from '../assets/weather/fog.svg?url';

const ASSETS = {
  sunny,
  nightClear,
  partlyCloudy,
  cloudy,
  rainy,
  storm,
  snow,
  fog,
};

/**
 * Map OpenWeather "main" + icon + description to a local illustration.
 */
export function weatherArtSrc({ condition = '', icon = '', description = '' }) {
  const main = String(condition).toLowerCase();
  const desc = String(description).toLowerCase();
  const ic = String(icon);

  if (main === 'thunderstorm') return ASSETS.storm;
  if (main === 'snow') return ASSETS.snow;
  if (main === 'rain' || main === 'drizzle') return ASSETS.rainy;
  if (
    main === 'mist' ||
    main === 'fog' ||
    main === 'haze' ||
    main === 'smoke' ||
    main === 'dust' ||
    main === 'sand' ||
    main === 'ash' ||
    main === 'squall' ||
    main === 'tornado'
  ) {
    return ASSETS.fog;
  }

  if (main === 'clear') {
    return ic.endsWith('n') ? ASSETS.nightClear : ASSETS.sunny;
  }

  if (main === 'clouds') {
    if (desc.includes('overcast') || ic.startsWith('04')) return ASSETS.cloudy;
    if (ic.startsWith('02') || ic.startsWith('03') || desc.includes('few') || desc.includes('scattered')) {
      return ASSETS.partlyCloudy;
    }
    return ASSETS.cloudy;
  }

  return ASSETS.partlyCloudy;
}
