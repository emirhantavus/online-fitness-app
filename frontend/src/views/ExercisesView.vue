<template>
    <div>
      <headerComponent/>
      <exercisesComponent/>
      <footerComponent/>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import exercisesComponent from '../components/exercisesVideos.vue';
import footerComponent from '../components/footerComponent.vue';
import headerComponent from '../components/headerComponent.vue';
export default defineComponent({    
  name:'Exercises',
  components:{
      exercisesComponent,
      headerComponent,
      footerComponent,
  },
});
</script>