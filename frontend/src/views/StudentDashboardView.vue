<template>
      <div id="app">
            <headerComponent/>
            <StudentDashboard />
            <footerComponent/>
      </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import StudentDashboard from '../components/studentDashboardComponent.vue'
import headerComponent from '../components/headerComponent.vue';
import footerComponent from '../components/footerComponent.vue';
export default defineComponent({
  name: 'App',
  components: {
    StudentDashboard,
    headerComponent,  
    footerComponent,
  },
})
</script>