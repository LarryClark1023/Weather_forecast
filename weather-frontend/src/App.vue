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

      <PreferencesBar
        :temp-celsius="tempCelsius"
        :wind-ms="windMs"
        :geo-loading="geoLoading"
        :busy="loading || geoLoading"
        @update:temp-celsius="onTempUnit"
        @update:wind-ms="onWindUnit"
        @geolocate="fetchByGeolocation"
      />

      <SearchBar
        v-model="cityInput"
        :loading="loading"
        :recent-cities="recentCities"
        @search="fetchWeatherByCity"
      />

      <p id="a11y-status" class="sr-only" aria-live="polite" aria-atomic="true">{{ a11yStatus }}</p>

      <div
        v-if="errorMessage"
        class="mt-8 rounded-xl border border-red-500/30 bg-red-950/40 px-4 py-3 text-center text-red-200"
        role="alert"
      >
        {{ errorMessage }}
      </div>

      <div v-if="bundle" class="mt-10 space-y-2">
        <WeatherCard
          :weather="bundle.current"
          :temp-celsius="tempCelsius"
          :wind-ms="windMs"
        />
        <ForecastSection
          :days="bundle.forecast"
          :temp-celsius="tempCelsius"
          :wind-ms="windMs"
        />
      </div>

      <AppFooter :meta="bundle?.meta || null" />
    </div>
  </div>
</template>

<script>
import { computed, ref } from 'vue';
import SearchBar from './components/SearchBar.vue';
import WeatherCard from './components/WeatherCard.vue';
import ForecastSection from './components/ForecastSection.vue';
import AppFooter from './components/AppFooter.vue';
import PreferencesBar from './components/PreferencesBar.vue';
import { getWeather, getWeatherByCoords } from './services/api.js';
import { loadPreferences, saveTempUnit, saveWindUnit } from './utils/preferences.js';
import { getRecentCities, addRecentCity } from './utils/recentCities.js';

export default {
  components: {
    SearchBar,
    WeatherCard,
    ForecastSection,
    AppFooter,
    PreferencesBar,
  },
  setup() {
    const bundle = ref(null);
    const errorMessage = ref(null);
    const loading = ref(false);
    const geoLoading = ref(false);
    const cityInput = ref('');
    const prefs = loadPreferences();
    const tempCelsius = ref(prefs.tempCelsius);
    const windMs = ref(prefs.windMetersPerSecond);
    const recentCities = ref(getRecentCities());

    const refreshRecent = () => {
      recentCities.value = getRecentCities();
    };

    const a11yStatus = computed(() => {
      if (loading.value || geoLoading.value) return 'Loading weather.';
      if (errorMessage.value) return `Error: ${errorMessage.value}`;
      if (bundle.value?.current?.city) {
        return `Weather loaded for ${bundle.value.current.city}.`;
      }
      return '';
    });

    const onTempUnit = (v) => {
      tempCelsius.value = v;
      saveTempUnit(v);
    };

    const onWindUnit = (v) => {
      windMs.value = v;
      saveWindUnit(v);
    };

    const handleApiError = (error) => {
      const status = error.response?.status;
      if (status === 429) {
        errorMessage.value = 'Too many requests. Please wait a minute and try again.';
        return;
      }
      const msg = error.response?.data?.error;
      errorMessage.value =
        msg ||
        'Something went wrong. Check the city name, your connection, and that the backend is running.';
    };

    const fetchWeatherByCity = async (city) => {
      errorMessage.value = null;
      bundle.value = null;
      loading.value = true;
      try {
        const { data } = await getWeather(city);
        bundle.value = data;
        addRecentCity(city);
        refreshRecent();
      } catch (error) {
        handleApiError(error);
      } finally {
        loading.value = false;
      }
    };

    const fetchByGeolocation = () => {
      if (!navigator.geolocation) {
        errorMessage.value = 'Geolocation is not supported in this browser.';
        return;
      }
      errorMessage.value = null;
      bundle.value = null;
      geoLoading.value = true;
      navigator.geolocation.getCurrentPosition(
        async (pos) => {
          try {
            const { latitude, longitude } = pos.coords;
            const { data } = await getWeatherByCoords(latitude, longitude);
            bundle.value = data;
            const c = data.current;
            if (c?.city) {
              const label = c.country ? `${c.city}, ${c.country}` : c.city;
              cityInput.value = label;
              addRecentCity(c.city);
              refreshRecent();
            }
          } catch (error) {
            handleApiError(error);
          } finally {
            geoLoading.value = false;
          }
        },
        () => {
          geoLoading.value = false;
          errorMessage.value =
            'Could not read your location. Allow location access in the browser, or search by city.';
        },
        { enableHighAccuracy: false, timeout: 15000, maximumAge: 600000 },
      );
    };

    return {
      bundle,
      errorMessage,
      loading,
      geoLoading,
      cityInput,
      tempCelsius,
      windMs,
      recentCities,
      a11yStatus,
      onTempUnit,
      onWindUnit,
      fetchWeatherByCity,
      fetchByGeolocation,
    };
  },
};
</script>

<style scoped>
h1 {
  font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
}
</style>
