<template>
  <div
    class="mx-auto mt-6 flex max-w-3xl flex-col gap-4 rounded-xl border border-white/10 bg-white/5 px-4 py-4 sm:flex-row sm:flex-wrap sm:items-center sm:justify-between"
  >
    <fieldset class="min-w-0 border-0 p-0">
      <legend class="sr-only">Temperature units</legend>
      <span class="mb-2 block text-xs font-medium uppercase tracking-wide text-slate-500 sm:mb-0 sm:mr-3 sm:inline">Temperature</span>
      <div class="inline-flex rounded-lg border border-white/10 p-0.5" role="group" aria-label="Temperature units">
        <button
          type="button"
          class="rounded-md px-3 py-1.5 text-sm font-medium transition"
          :class="tempCelsius ? 'bg-sky-600 text-white' : 'text-slate-400 hover:text-white'"
          :aria-pressed="tempCelsius"
          @click="$emit('update:tempCelsius', true)"
        >
          °C
        </button>
        <button
          type="button"
          class="rounded-md px-3 py-1.5 text-sm font-medium transition"
          :class="!tempCelsius ? 'bg-sky-600 text-white' : 'text-slate-400 hover:text-white'"
          :aria-pressed="!tempCelsius"
          @click="$emit('update:tempCelsius', false)"
        >
          °F
        </button>
      </div>
    </fieldset>

    <fieldset class="min-w-0 border-0 p-0">
      <legend class="sr-only">Wind speed units</legend>
      <span class="mb-2 block text-xs font-medium uppercase tracking-wide text-slate-500 sm:mb-0 sm:mr-3 sm:inline">Wind</span>
      <div class="inline-flex rounded-lg border border-white/10 p-0.5" role="group" aria-label="Wind speed units">
        <button
          type="button"
          class="rounded-md px-3 py-1.5 text-sm font-medium transition"
          :class="windMs ? 'bg-sky-600 text-white' : 'text-slate-400 hover:text-white'"
          :aria-pressed="windMs"
          @click="$emit('update:windMs', true)"
        >
          m/s
        </button>
        <button
          type="button"
          class="rounded-md px-3 py-1.5 text-sm font-medium transition"
          :class="!windMs ? 'bg-sky-600 text-white' : 'text-slate-400 hover:text-white'"
          :aria-pressed="!windMs"
          @click="$emit('update:windMs', false)"
        >
          mph
        </button>
      </div>
    </fieldset>

    <button
      type="button"
      class="rounded-lg border border-emerald-500/40 bg-emerald-950/30 px-4 py-2 text-sm font-medium text-emerald-200 transition hover:bg-emerald-900/40 disabled:cursor-not-allowed disabled:opacity-50"
      :disabled="busy"
      aria-label="Use my current location for weather"
      @click="$emit('geolocate')"
    >
      {{ geoLoading ? 'Locating…' : 'Use my location' }}
    </button>
  </div>
</template>

<script>
export default {
  props: {
    tempCelsius: { type: Boolean, default: true },
    windMs: { type: Boolean, default: true },
    geoLoading: { type: Boolean, default: false },
    busy: { type: Boolean, default: false },
  },
  emits: ['update:tempCelsius', 'update:windMs', 'geolocate'],
};
</script>
