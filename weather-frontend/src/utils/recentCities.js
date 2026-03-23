const KEY = 'wf_recent_cities';
const MAX = 8;

export function getRecentCities() {
  if (typeof localStorage === 'undefined') return [];
  try {
    const raw = localStorage.getItem(KEY);
    const list = raw ? JSON.parse(raw) : [];
    return Array.isArray(list) ? list : [];
  } catch {
    return [];
  }
}

export function addRecentCity(name) {
  if (typeof localStorage === 'undefined') return;
  const n = String(name || '').trim();
  if (!n) return;
  const list = getRecentCities();
  const next = [n, ...list.filter((x) => String(x).toLowerCase() !== n.toLowerCase())].slice(0, MAX);
  localStorage.setItem(KEY, JSON.stringify(next));
}
