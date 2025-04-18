<template>
      <div>
        <headerComponent />
        <div class="main-content">
          <trainerLoginComponent />
        </div>
        <footerComponent />
      </div>
</template>
    
<script lang="ts">
    import { defineComponent } from 'vue';
    import footerComponent from '../components/footerComponent.vue';
    import headerComponent from '../components/headerComponent.vue';
    import trainerLoginComponent from '../components/trainerLoginComponent.vue';
    
    export default defineComponent({
          name: 'App',
          components: {
                trainerLoginComponent,
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