const TEMP_KEY = 'wf_temp_celsius';
const WIND_KEY = 'wf_wind_ms';

export function loadPreferences() {
  if (typeof localStorage === 'undefined') {
    return { tempCelsius: true, windMetersPerSecond: true };
  }
  return {
    tempCelsius: localStorage.getItem(TEMP_KEY) !== 'false',
    windMetersPerSecond: localStorage.getItem(WIND_KEY) !== 'false',
  };
}

export function saveTempUnit(useCelsius) {
  if (typeof localStorage === 'undefined') return;
  localStorage.setItem(TEMP_KEY, String(useCelsius));
}

export function saveWindUnit(useMetersPerSecond) {
  if (typeof localStorage === 'undefined') return;
  localStorage.setItem(WIND_KEY, String(useMetersPerSecond));
}
