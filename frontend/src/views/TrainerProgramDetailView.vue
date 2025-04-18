<template>
      <div>
        <headerComponent />
        <div class="main-content">
          <trainerPDComponent />
        </div>
        <footerComponent />
      </div>
</template>
    
<script lang="ts">
    import { defineComponent } from 'vue';
    import trainerPDComponent from '../components/trainerPDComponent.vue';
    import footerComponent from '../components/footerComponent.vue';
    import headerComponent from '../components/headerComponent.vue';
    
    export default defineComponent({
          name: 'planView',
          components: {
                trainerPDComponent,
                footerComponent,
                headerComponent,
          }
    })
</script>