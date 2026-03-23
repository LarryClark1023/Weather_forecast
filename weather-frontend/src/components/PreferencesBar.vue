<template>
  <div
    class="mx-auto mt-6 flex max-w-3xl flex-col gap-4 rounded-xl border border-slate-200 bg-white/80 px-4 py-4 shadow-sm backdrop-blur-sm dark:border-white/10 dark:bg-white/5 dark:shadow-none sm:flex-row sm:flex-wrap sm:items-center sm:justify-between"
  >
    <fieldset class="min-w-0 border-0 p-0">
      <legend class="sr-only">Color theme</legend>
      <span
        class="mb-2 block text-xs font-medium uppercase tracking-wide text-slate-500 dark:text-slate-500 sm:mb-0 sm:mr-3 sm:inline"
        >Theme</span
      >
      <div
        class="inline-flex rounded-lg border border-slate-200 p-0.5 dark:border-white/10"
        role="group"
        aria-label="Color theme"
      >
        <button
          v-for="opt in themeOptions"
          :key="opt.value"
          type="button"
          class="rounded-md px-2.5 py-1.5 text-sm font-medium transition sm:px-3"
          :class="
            themeMode === opt.value
              ? 'bg-sky-600 text-white'
              : 'text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white'
          "
          :aria-pressed="themeMode === opt.value"
          @click="$emit('update:themeMode', opt.value)"
        >
          {{ opt.label }}
        </button>
      </div>
    </fieldset>

    <fieldset class="min-w-0 border-0 p-0">
      <legend class="sr-only">Temperature units</legend>
      <span
        class="mb-2 block text-xs font-medium uppercase tracking-wide text-slate-500 dark:text-slate-500 sm:mb-0 sm:mr-3 sm:inline"
        >Temperature</span
      >
      <div
        class="inline-flex rounded-lg border border-slate-200 p-0.5 dark:border-white/10"
        role="group"
        aria-label="Temperature units"
      >
        <button
          type="button"
          class="rounded-md px-3 py-1.5 text-sm font-medium transition"
          :class="tempCelsius ? 'bg-sky-600 text-white' : 'text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white'"
          :aria-pressed="tempCelsius"
          @click="$emit('update:tempCelsius', true)"
        >
          °C
        </button>
        <button
          type="button"
          class="rounded-md px-3 py-1.5 text-sm font-medium transition"
          :class="!tempCelsius ? 'bg-sky-600 text-white' : 'text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white'"
          :aria-pressed="!tempCelsius"
          @click="$emit('update:tempCelsius', false)"
        >
          °F
        </button>
      </div>
    </fieldset>

    <fieldset class="min-w-0 border-0 p-0">
      <legend class="sr-only">Wind speed units</legend>
      <span
        class="mb-2 block text-xs font-medium uppercase tracking-wide text-slate-500 dark:text-slate-500 sm:mb-0 sm:mr-3 sm:inline"
        >Wind</span
      >
      <div
        class="inline-flex rounded-lg border border-slate-200 p-0.5 dark:border-white/10"
        role="group"
        aria-label="Wind speed units"
      >
        <button
          type="button"
          class="rounded-md px-3 py-1.5 text-sm font-medium transition"
          :class="windMs ? 'bg-sky-600 text-white' : 'text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white'"
          :aria-pressed="windMs"
          @click="$emit('update:windMs', true)"
        >
          m/s
        </button>
        <button
          type="button"
          class="rounded-md px-3 py-1.5 text-sm font-medium transition"
          :class="!windMs ? 'bg-sky-600 text-white' : 'text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white'"
          :aria-pressed="!windMs"
          @click="$emit('update:windMs', false)"
        >
          mph
        </button>
      </div>
    </fieldset>

    <button
      type="button"
      class="rounded-lg border border-emerald-600/40 bg-emerald-50 px-4 py-2 text-sm font-medium text-emerald-900 transition hover:bg-emerald-100 disabled:cursor-not-allowed disabled:opacity-50 dark:border-emerald-500/40 dark:bg-emerald-950/30 dark:text-emerald-200 dark:hover:bg-emerald-900/40"
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
    themeMode: { type: String, default: 'dark' },
    tempCelsius: { type: Boolean, default: true },
    windMs: { type: Boolean, default: true },
    geoLoading: { type: Boolean, default: false },
    busy: { type: Boolean, default: false },
  },
  emits: ['update:themeMode', 'update:tempCelsius', 'update:windMs', 'geolocate'],
  data() {
    return {
      themeOptions: [
        { value: 'light', label: 'Light' },
        { value: 'dark', label: 'Dark' },
        { value: 'system', label: 'System' },
      ],
    };
  },
};
</script>
