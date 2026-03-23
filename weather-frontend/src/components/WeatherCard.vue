<template>
  <section
    class="overflow-hidden rounded-2xl border border-white/10 bg-white/5 p-6 shadow-xl backdrop-blur-md sm:p-8"
    aria-labelledby="current-weather-heading"
  >
    <div class="flex flex-col gap-6 sm:flex-row sm:items-start sm:justify-between">
      <div>
        <p class="text-sm font-medium uppercase tracking-wide text-sky-300/90">Right now</p>
        <h2 id="current-weather-heading" class="mt-1 text-3xl font-bold text-white sm:text-4xl">
          {{ weather.city }}<span v-if="weather.country" class="text-slate-400">, {{ weather.country }}</span>
        </h2>
        <p class="mt-1 capitalize text-slate-300">{{ weather.description }}</p>
      </div>
      <div class="flex items-center gap-4">
        <WeatherIllustration
          :condition="weather.condition"
          :icon="weather.icon"
          :description="weather.description"
          class="h-28 w-28 shrink-0 drop-shadow-[0_8px_24px_rgba(0,0,0,0.35)] sm:h-32 sm:w-32"
        />
        <div>
          <p class="text-5xl font-light leading-none text-white sm:text-6xl">
            {{ formatTemp(weather.temperature) }}°
          </p>
          <p class="mt-2 text-sm text-slate-400">
            Feels like {{ formatTemp(weather.feels_like) }}{{ tempSuffix }}
          </p>
        </div>
      </div>
    </div>

    <dl
      class="mt-8 grid grid-cols-2 gap-4 border-t border-white/10 pt-6 sm:grid-cols-4"
    >
      <div class="rounded-xl bg-black/20 px-4 py-3">
        <dt class="text-xs font-medium uppercase tracking-wide text-slate-500">Condition</dt>
        <dd class="mt-1 font-semibold text-white">{{ weather.condition }}</dd>
      </div>
      <div class="rounded-xl bg-black/20 px-4 py-3">
        <dt class="text-xs font-medium uppercase tracking-wide text-slate-500">Humidity</dt>
        <dd class="mt-1 font-semibold text-white">{{ weather.humidity }}%</dd>
      </div>
      <div class="rounded-xl bg-black/20 px-4 py-3">
        <dt class="text-xs font-medium uppercase tracking-wide text-slate-500">Wind</dt>
        <dd class="mt-1 font-semibold text-white">{{ formatWind(weather.wind_speed) }} {{ windSuffix }}</dd>
      </div>
      <div class="rounded-xl bg-black/20 px-4 py-3">
        <dt class="text-xs font-medium uppercase tracking-wide text-slate-500">Comfort</dt>
        <dd class="mt-1 font-semibold text-white">{{ comfortLabel }}</dd>
      </div>
    </dl>
  </section>
</template>

<script>
import WeatherIllustration from './WeatherIllustration.vue';
import {
  formatTempCelsius,
  formatWindMs,
  tempUnitSuffix,
  windUnitSuffix,
} from '../utils/displayUnits.js';

export default {
  components: { WeatherIllustration },
  props: {
    weather: {
      type: Object,
      required: true,
    },
    tempCelsius: { type: Boolean, default: true },
    windMs: { type: Boolean, default: true },
  },
  computed: {
    tempSuffix() {
      return tempUnitSuffix(this.tempCelsius);
    },
    windSuffix() {
      return windUnitSuffix(this.windMs);
    },
    comfortLabel() {
      const t = this.weather.feels_like;
      if (typeof t !== 'number') return '—';
      if (t <= 0) return 'Cold';
      if (t <= 15) return 'Cool';
      if (t <= 25) return 'Mild';
      if (t <= 32) return 'Warm';
      return 'Hot';
    },
  },
  methods: {
    formatTemp(v) {
      return formatTempCelsius(v, this.tempCelsius);
    },
    formatWind(v) {
      return formatWindMs(v, this.windMs);
    },
  },
};
</script>
