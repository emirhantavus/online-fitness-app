<template>
      <div>
        <headerComponent />
        <div class="main-content">
          <programDetailComponent />
        </div>
        <footerComponent />
      </div>
</template>
    
<script lang="ts">
    import { defineComponent } from 'vue';
    import programDetailComponent from '../components/studentPDComponent.vue';
    import footerComponent from '../components/footerComponent.vue';
    import headerComponent from '../components/headerComponent.vue';
    
    export default defineComponent({
          name: 'planView',
          components: {
                programDetailComponent,
                footerComponent,
                headerComponent,
          }
    })
</script>