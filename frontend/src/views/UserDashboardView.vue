<template>
      <div id="app">
            <headerComponent/>
              <UserDashboard />
            <footerComponent/>
      </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import UserDashboard from '../components/userDashboardComponent.vue'
import headerComponent from '../components/headerComponent.vue';
import footerComponent from '../components/footerComponent.vue';
export default defineComponent({
  name: 'App',
  components: {
    UserDashboard,
    headerComponent,
    footerComponent,
  },
})
</script>