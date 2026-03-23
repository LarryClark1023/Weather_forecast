export function formatTempCelsius(c, useCelsius) {
  if (typeof c !== 'number' || Number.isNaN(c)) return c;
  if (useCelsius) return Math.round(c * 10) / 10;
  return Math.round(((c * 9) / 5 + 32) * 10) / 10;
}

export function tempUnitSuffix(useCelsius) {
  return useCelsius ? '°C' : '°F';
}

export function formatWindMs(ms, useMetersPerSecond) {
  if (typeof ms !== 'number' || Number.isNaN(ms)) return ms;
  if (useMetersPerSecond) return Math.round(ms * 10) / 10;
  return Math.round(ms * 2.236936 * 10) / 10;
}

export function windUnitSuffix(useMetersPerSecond) {
  return useMetersPerSecond ? 'm/s' : 'mph';
}
