<template>
  <div>
    <HeaderComponent />
    <ExerciseDetail />
    <FooterComponent />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import ExerciseDetail from '@/components/exerciseVideoDetail.vue';
import FooterComponent from '@/components/footerComponent.vue';
import HeaderComponent from '@/components/headerComponent.vue';
      
export default defineComponent({
  name: 'ExerciseDetailPage',
  components: {
    ExerciseDetail,
    HeaderComponent,
    FooterComponent,
  }
});
</script>

