<template>
      <div id="app">
        <headerComponent/>
        <foodCalorieComponent />
      </div>
    </template>
    
    <script lang="ts">
    import { defineComponent } from 'vue';
    import foodCalorieComponent from '../components/foodCalorieComponent.vue';
    import headerComponent from '../components/headerComponent.vue';
    import footerComponent from '../components/footerComponent.vue';
    export default defineComponent({
      name: 'App',
      components: {
        foodCalorieComponent,
        headerComponent,
        footerComponent,
      },
    })
    </script>

    