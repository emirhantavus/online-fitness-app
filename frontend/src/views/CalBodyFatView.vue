<template>
      <div>
        <headerComponent />
        <div class="main-content">
          <calculateBodyFat />
        </div>
        <footerComponent />
      </div>
</template>
    
<script lang="ts">
import { defineComponent } from 'vue';
import calculateBodyFat from '../components/calculateBodyFat.vue';
import footerComponent from '../components/footerComponent.vue';
import headerComponent from '../components/headerComponent.vue';

export default defineComponent({
      name: 'planView',
      components: {
            calculateBodyFat,
            footerComponent,
            headerComponent,
      }
})
</script>