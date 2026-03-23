<template>
  <img :src="src" :alt="altText" :class="imgClass" draggable="false" />
</template>

<script>
import { weatherArtSrc } from '../utils/weatherArt.js';

export default {
  props: {
    condition: {
      type: String,
      default: '',
    },
    icon: {
      type: String,
      default: '',
    },
    description: {
      type: String,
      default: '',
    },
    imgClass: {
      type: String,
      default: '',
    },
  },
  computed: {
    src() {
      return weatherArtSrc({
        condition: this.condition,
        icon: this.icon,
        description: this.description,
      });
    },
    altText() {
      return this.description || this.condition || 'Weather';
    },
  },
};
</script>
