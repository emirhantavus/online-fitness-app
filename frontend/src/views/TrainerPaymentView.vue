<template>
      <headerComponent/>
      <trainerPaymentComponent />
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue';
  import trainerPaymentComponent from '../components/trainerPaymentComponent.vue';
  import headerComponent from '../components/headerComponent.vue';
  import footerComponent from '../components/footerComponent.vue';
  export default defineComponent({
    name: 'App',
    components: {
      trainerPaymentComponent,
      headerComponent,
      footerComponent,
    },
  })
  </script>
  
      