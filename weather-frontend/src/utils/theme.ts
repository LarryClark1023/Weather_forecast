import type { ThemeMode } from './preferences';
import { loadThemeMode, saveThemeMode } from './preferences';

function prefersDark(): boolean {
  return window.matchMedia('(prefers-color-scheme: dark)').matches;
}

export function isDarkEffective(mode: ThemeMode): boolean {
  if (mode === 'dark') return true;
  if (mode === 'light') return false;
  return prefersDark();
}

export function applyThemeToDocument(mode: ThemeMode): void {
  document.documentElement.classList.toggle('dark', isDarkEffective(mode));
}

export function setThemeMode(mode: ThemeMode): void {
  saveThemeMode(mode);
  applyThemeToDocument(mode);
}

export function initTheme(): void {
  if (typeof document === 'undefined') return;
  applyThemeToDocument(loadThemeMode());
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    if (loadThemeMode() === 'system') applyThemeToDocument('system');
  });
}
