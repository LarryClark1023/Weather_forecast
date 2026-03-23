<template>
  <section class="mt-10">
    <div class="mb-4 flex flex-wrap items-end justify-between gap-2">
      <div>
        <h3 class="text-lg font-semibold text-white">Next 6 days</h3>
        <p class="text-sm text-slate-400">
          Starting tomorrow — today is not included. Each day shows daily high and low (°C).
        </p>
      </div>
      <p v-if="days.length > 0 && days.length < 6" class="max-w-xs text-right text-xs text-slate-500">
        Showing {{ days.length }} of 6 days — forecast data was incomplete for this location.
      </p>
    </div>

    <div
      v-if="days.length === 0"
      class="rounded-xl border border-dashed border-white/15 bg-white/5 px-4 py-8 text-center text-slate-400"
    >
      No multi-day forecast available for this search.
    </div>

    <div
      v-else
      class="flex gap-3 overflow-x-auto pb-2 sm:grid sm:grid-cols-2 sm:overflow-visible md:grid-cols-3 lg:grid-cols-6"
    >
      <article
        v-for="day in days"
        :key="day.date"
        class="min-w-[8.5rem] flex-shrink-0 rounded-xl border border-white/10 bg-white/5 p-4 text-center backdrop-blur-sm"
      >
        <p class="text-xs font-medium uppercase tracking-wide text-sky-300">{{ day.weekday }}</p>
        <p class="text-sm text-slate-400">{{ day.label }}</p>

        <WeatherIllustration
          :condition="day.condition"
          :icon="day.icon"
          :description="day.description"
          class="mx-auto mt-2 h-16 w-16 drop-shadow-md"
        />

        <div class="mt-3 space-y-2 border-t border-white/10 pt-3">
          <div class="flex items-center justify-between gap-2 text-sm">
            <span class="text-xs font-semibold uppercase tracking-wide text-rose-300/90">High</span>
            <span class="text-lg font-bold text-white">{{ day.temp_max }}°</span>
          </div>
          <div class="flex items-center justify-between gap-2 text-sm">
            <span class="text-xs font-semibold uppercase tracking-wide text-sky-300/90">Low</span>
            <span class="text-lg font-semibold text-sky-100">{{ day.temp_min }}°</span>
          </div>
        </div>

        <p class="mt-3 line-clamp-2 text-xs capitalize text-slate-400">{{ day.description }}</p>
        <p class="mt-2 text-[11px] text-slate-500">
          Humidity ~{{ day.humidity }}% · Wind {{ day.wind_speed }} m/s
        </p>
      </article>
    </div>
  </section>
</template>

<script>
import WeatherIllustration from './WeatherIllustration.vue';

export default {
  components: { WeatherIllustration },
  props: {
    days: {
      type: Array,
      default: () => [],
    },
  },
};
</script>
