<template>
  <div>
    <headerComponent />
    <div class="main-content">
      <planComponent />
    </div>
    <footerComponent />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import planComponent from '../components/subPlanComponent.vue';
import footerComponent from '../components/footerComponent.vue';
import headerComponent from '../components/headerComponent.vue';

export default defineComponent({
      name: 'planView',
      components: {
            planComponent,
            footerComponent,
            headerComponent,
      }
})
</script>

<style scoped>
.main-content {
  padding: 20px;
  background-color: #f5f5f5;
}
</style>