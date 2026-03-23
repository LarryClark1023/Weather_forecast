<template>
  <div class="mx-auto mt-6 max-w-xl">
    <label for="city-search" class="sr-only">City name</label>
    <div class="flex flex-col gap-2 sm:flex-row sm:items-stretch">
      <div class="flex min-w-0 flex-1">
        <input
          id="city-search"
          v-model="city"
          type="text"
          name="city"
          autocomplete="address-level2"
          placeholder="Enter city name"
          :disabled="loading"
          :aria-invalid="validationError ? 'true' : 'false'"
          :aria-describedby="ariaDescribedBy"
          class="w-full rounded-l-xl border border-white/10 bg-white/5 px-4 py-3 text-slate-100 placeholder:text-slate-500 outline-none ring-sky-400/40 transition focus:border-sky-400/50 focus:ring-2 disabled:opacity-50"
          @input="onInput"
          @keyup.enter="searchWeather"
        />
        <button
          type="button"
          :disabled="loading"
          class="rounded-r-xl bg-sky-500 px-6 py-3 font-medium text-white transition hover:bg-sky-400 disabled:cursor-not-allowed disabled:opacity-50"
          aria-label="Search weather for this city"
          @click="searchWeather"
        >
          {{ loading ? 'Loading…' : 'Search' }}
        </button>
      </div>
    </div>
    <p id="city-search-hint" class="mt-2 text-center text-xs text-slate-500">
      Search by city name, pick a recent city below, or use your location.
    </p>
    <p
      v-if="validationError"
      id="city-search-error"
      class="mt-1 text-center text-sm text-amber-400"
      role="alert"
    >
      {{ validationError }}
    </p>

    <div v-if="recentCities.length" class="mt-4">
      <p class="mb-2 text-center text-xs font-medium uppercase tracking-wide text-slate-500">
        Recent
      </p>
      <div class="flex flex-wrap justify-center gap-2" role="list">
        <button
          v-for="c in recentCities"
          :key="c"
          type="button"
          class="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-sm text-slate-300 transition hover:border-sky-500/40 hover:text-white disabled:opacity-50"
          :disabled="loading"
          role="listitem"
          @click="selectRecent(c)"
        >
          {{ c }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    loading: {
      type: Boolean,
      default: false,
    },
    recentCities: {
      type: Array,
      default: () => [],
    },
    modelValue: {
      type: String,
      default: '',
    },
  },
  emits: ['search', 'update:modelValue'],
  computed: {
    ariaDescribedBy() {
      return this.validationError ? 'city-search-hint city-search-error' : 'city-search-hint';
    },
  },
  data() {
    return {
      city: this.modelValue,
      validationError: '',
    };
  },
  watch: {
    modelValue(v) {
      this.city = v;
    },
  },
  methods: {
    onInput() {
      this.$emit('update:modelValue', this.city);
    },
    searchWeather() {
      this.validationError = '';
      const trimmed = this.city.trim();
      if (!trimmed) {
        this.validationError = 'Please enter a city name.';
        return;
      }
      this.$emit('search', trimmed);
    },
    selectRecent(c) {
      this.city = c;
      this.$emit('update:modelValue', c);
      this.validationError = '';
      this.$emit('search', c.trim());
    },
  },
};
</script>
