<template>
      <div id="app">
            <headerComponent/>
              <trainerComponent />
            <footerComponent/>
      </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import trainerComponent from '../components/trainerListComponent.vue'
import headerComponent from '../components/headerComponent.vue';
import footerComponent from '../components/footerComponent.vue';
export default defineComponent({
  name: 'App',
  components: {
    trainerComponent,
    headerComponent,
    footerComponent,
  },
})
</script>