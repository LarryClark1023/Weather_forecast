<template>
  <footer
    class="mt-12 border-t border-white/10 pt-6 text-center text-xs leading-relaxed text-slate-500"
  >
    <p class="font-medium text-slate-400">Data sources</p>
    <ul class="mt-2 flex flex-wrap justify-center gap-x-4 gap-y-1">
      <li v-for="s in sources" :key="s.id">
        <a
          :href="s.url"
          class="text-sky-400/90 underline-offset-2 hover:text-sky-300 hover:underline"
          target="_blank"
          rel="noopener noreferrer"
          >{{ s.label }}</a
        >
        <span class="text-slate-600"> — {{ s.role }}</span>
      </li>
    </ul>
    <p v-if="note" class="mx-auto mt-3 max-w-2xl text-slate-500">{{ note }}</p>
    <p v-if="fetchedAt" class="mt-3 text-slate-600">
      Last updated (server time, UTC):
      <time :datetime="fetchedAt">{{ formattedTime }}</time>
      <span v-if="cacheHit" class="ml-1 text-slate-500">(served from cache)</span>
    </p>
    <p v-else class="mt-3 text-slate-600">Search a city or use your location to load timestamps from the API.</p>
  </footer>
</template>

<script>
const DEFAULT_SOURCES = [
  {
    id: 'openweathermap',
    label: 'OpenWeatherMap',
    url: 'https://openweathermap.org/',
    role: 'Current weather and 5-day / 3-hour forecast',
  },
  {
    id: 'open-meteo',
    label: 'Open-Meteo',
    url: 'https://open-meteo.com/',
    role: 'Daily values used to complete the 6-day outlook when needed',
  },
];

const DEFAULT_NOTE =
  'Six-day outlook starts tomorrow (today excluded). Open-Meteo may supply later days when the free OpenWeatherMap window ends.';

export default {
  props: {
    meta: {
      type: Object,
      default: null,
    },
  },
  computed: {
    sources() {
      return this.meta?.sources?.length ? this.meta.sources : DEFAULT_SOURCES;
    },
    note() {
      return this.meta?.note || DEFAULT_NOTE;
    },
    fetchedAt() {
      return this.meta?.fetched_at || '';
    },
    cacheHit() {
      return Boolean(this.meta?.cache_hit);
    },
    formattedTime() {
      if (!this.fetchedAt) return '';
      try {
        const d = new Date(this.fetchedAt);
        return Number.isNaN(d.getTime()) ? this.fetchedAt : d.toLocaleString();
      } catch {
        return this.fetchedAt;
      }
    },
  },
};
</script>
