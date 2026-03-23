const TEMP_KEY = 'wf_temp_celsius';
const WIND_KEY = 'wf_wind_ms';
const THEME_KEY = 'wf_color_mode';

export type ThemeMode = 'light' | 'dark' | 'system';

export function loadThemeMode(): ThemeMode {
  if (typeof localStorage === 'undefined') return 'dark';
  const v = localStorage.getItem(THEME_KEY);
  if (v === 'light' || v === 'dark' || v === 'system') return v;
  return 'dark';
}

export function saveThemeMode(mode: ThemeMode): void {
  if (typeof localStorage === 'undefined') return;
  localStorage.setItem(THEME_KEY, mode);
}

export function loadPreferences(): {
  tempCelsius: boolean;
  windMetersPerSecond: boolean;
  themeMode: ThemeMode;
} {
  if (typeof localStorage === 'undefined') {
    return { tempCelsius: true, windMetersPerSecond: true, themeMode: 'dark' };
  }
  return {
    tempCelsius: localStorage.getItem(TEMP_KEY) !== 'false',
    windMetersPerSecond: localStorage.getItem(WIND_KEY) !== 'false',
    themeMode: loadThemeMode(),
  };
}

export function saveTempUnit(useCelsius: boolean): void {
  if (typeof localStorage === 'undefined') return;
  localStorage.setItem(TEMP_KEY, String(useCelsius));
}

export function saveWindUnit(useMetersPerSecond: boolean): void {
  if (typeof localStorage === 'undefined') return;
  localStorage.setItem(WIND_KEY, String(useMetersPerSecond));
}
