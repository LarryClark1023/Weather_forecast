<template>
  <section
    class="overflow-hidden rounded-2xl border border-white/10 bg-white/5 p-6 shadow-xl backdrop-blur-md sm:p-8"
  >
    <div class="flex flex-col gap-6 sm:flex-row sm:items-start sm:justify-between">
      <div>
        <p class="text-sm font-medium uppercase tracking-wide text-sky-300/90">Right now</p>
        <h2 class="mt-1 text-3xl font-bold text-white sm:text-4xl">
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
          <p class="mt-2 text-sm text-slate-400">Feels like {{ formatTemp(weather.feels_like) }}°C</p>
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
        <dd class="mt-1 font-semibold text-white">{{ weather.wind_speed }} m/s</dd>
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

export default {
  components: { WeatherIllustration },
  props: {
    weather: {
      type: Object,
      required: true,
    },
  },
  computed: {
    comfortLabel() {
      const t = this.weather.feels_like;
      if (t <= 0) return 'Cold';
      if (t <= 15) return 'Cool';
      if (t <= 25) return 'Mild';
      if (t <= 32) return 'Warm';
      return 'Hot';
    },
  },
  methods: {
    formatTemp(v) {
      return typeof v === 'number' ? Math.round(v * 10) / 10 : v;
    },
  },
};
</script>
