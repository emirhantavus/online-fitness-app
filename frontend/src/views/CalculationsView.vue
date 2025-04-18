<template>
  <div>
    <HeaderComponent />
    <CalculationComponent />
    <FooterComponent />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import FooterComponent from '@/components/footerComponent.vue';
import CalculationComponent from '@/components/calculationsComponent.vue';
import HeaderComponent from '@/components/headerComponent.vue';
      
export default defineComponent({
  name: 'ExerciseDetailPage',
  components: {
    CalculationComponent,
    HeaderComponent,
    FooterComponent,
  }
});
</script>
    
    