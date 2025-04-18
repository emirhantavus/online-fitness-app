<template>
      <div id="app">
            <headerComponent/>
            <TrainerDashboard />
            <footerComponent/>
      </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import TrainerDashboard from '../components/trainerDashboardComponent.vue'
import headerComponent from '../components/headerComponent.vue';
import footerComponent from '../components/footerComponent.vue';
export default defineComponent({
  name: 'App',
  components: {
    TrainerDashboard,
    headerComponent,
    footerComponent,
  },
})
</script>