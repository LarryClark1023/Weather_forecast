<template>
  <div class="mx-auto mt-8 max-w-xl">
    <div class="flex flex-col gap-2 sm:flex-row sm:items-stretch">
      <div class="flex min-w-0 flex-1">
        <input
          v-model="city"
          type="text"
          placeholder="Enter city name"
          :disabled="loading"
          class="w-full rounded-l-xl border border-white/10 bg-white/5 px-4 py-3 text-slate-100 placeholder:text-slate-500 outline-none ring-sky-400/40 transition focus:border-sky-400/50 focus:ring-2 disabled:opacity-50"
          @keyup.enter="searchWeather"
        />
        <button
          type="button"
          :disabled="loading"
          class="rounded-r-xl bg-sky-500 px-6 py-3 font-medium text-white transition hover:bg-sky-400 disabled:cursor-not-allowed disabled:opacity-50"
          @click="searchWeather"
        >
          {{ loading ? 'Loading…' : 'Search' }}
        </button>
      </div>
    </div>
    <p v-if="validationError" class="mt-2 text-center text-sm text-amber-400">
      {{ validationError }}
    </p>
  </div>
</template>

<script>
export default {
  props: {
    loading: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      city: '',
      validationError: '',
    };
  },
  methods: {
    searchWeather() {
      this.validationError = '';
      const trimmed = this.city.trim();
      if (!trimmed) {
        this.validationError = 'Please enter a city name.';
        return;
      }
      this.$emit('search', trimmed);
    },
  },
};
</script>
