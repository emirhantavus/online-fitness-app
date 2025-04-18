<template>
      <footer>
        <div class="container">
          <p>&copy; {{ currentYear }} FitCamp Fitness App. All rights reserved.</p>
        </div>
      </footer>
    </template>
    
    <script lang="ts">
    import { defineComponent } from 'vue';
    
    export default defineComponent({
      data() {
        return {
          currentYear: new Date().getFullYear(),
        };
      },
    });
    </script>
    

<style scoped>
footer {
      background-color: #f5f5f5;
      padding: 20px;
      text-align: center;
}
</style>