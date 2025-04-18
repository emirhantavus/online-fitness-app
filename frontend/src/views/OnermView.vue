<template>
      <headerComponent/>
      <div>
        <onermComponent />
      </div>
      <footerComponent/>
    </template>
    
    <script lang="ts">
    import { defineComponent } from 'vue';
    import onermComponent from '../components/onermComponent.vue'
    import headerComponent from '@/components/headerComponent.vue';
    import footerComponent from '@/components/footerComponent.vue';

    export default defineComponent({
      name: '1RMPage',
      components: {
        onermComponent,
        headerComponent,
        footerComponent,
      },
    });
    </script>
    
    <style scoped>
    
    </style>
    