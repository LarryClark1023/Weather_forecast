<template>
  <div
    class="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-sky-950 text-slate-100"
  >
    <div class="container mx-auto max-w-5xl px-4 py-10 pb-16">
      <header class="text-center">
        <p class="text-sm font-medium uppercase tracking-[0.2em] text-sky-400/80">Live weather</p>
        <h1 class="mt-2 text-3xl font-bold tracking-tight text-white sm:text-4xl">
          Weather forecast
        </h1>
        <p class="mx-auto mt-3 max-w-lg text-slate-400">
          Current conditions and up to six forecast days (tomorrow onward; today excluded).
        </p>
      </header>

      <SearchBar :loading="loading" @search="fetchWeather" />

      <div
        v-if="errorMessage"
        class="mt-8 rounded-xl border border-red-500/30 bg-red-950/40 px-4 py-3 text-center text-red-200"
        role="alert"
      >
        {{ errorMessage }}
      </div>

      <div v-if="bundle" class="mt-10 space-y-2">
        <WeatherCard :weather="bundle.current" />
        <ForecastSection :days="bundle.forecast" />
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import SearchBar from './components/SearchBar.vue';
import WeatherCard from './components/WeatherCard.vue';
import ForecastSection from './components/ForecastSection.vue';
import { getWeather } from './services/api.js';

export default {
  components: {
    SearchBar,
    WeatherCard,
    ForecastSection,
  },
  setup() {
    const bundle = ref(null);
    const errorMessage = ref(null);
    const loading = ref(false);

    const fetchWeather = async (city) => {
      errorMessage.value = null;
      bundle.value = null;
      loading.value = true;
      try {
        const { data } = await getWeather(city);
        bundle.value = data;
      } catch (error) {
        const msg = error.response?.data?.error;
        errorMessage.value =
          msg || 'Something went wrong. Check the city name and that the backend is running.';
      } finally {
        loading.value = false;
      }
    };

    return {
      bundle,
      errorMessage,
      loading,
      fetchWeather,
    };
  },
};
</script>

<style scoped>
h1 {
  font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
}
</style>
