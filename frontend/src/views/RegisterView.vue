<template>
      <div id="app">
      <headerComponent/>
        <registerPage />
      <footerComponent/>
      </div>
    </template>
    
    <script lang="ts">
    import { defineComponent } from 'vue';
    import registerPage from '../components/registerPage.vue';
    import headerComponent from '../components/headerComponent.vue';
    import footerComponent from '../components/footerComponent.vue';
    export default defineComponent({
      name: 'App',
      components: {
        registerPage,
        headerComponent,
        footerComponent,
      },
    })
    </script>

    