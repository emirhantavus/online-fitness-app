<template>
  <div class="home-view">
    <headerComponent/>
    <homePage />
    <router-view />
    <footerComponent/>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import homePage from '../components/homePage.vue';
import footerComponent from '../components/footerComponent.vue';
import headerComponent from '../components/headerComponent.vue';
export default defineComponent({
  name:'HomeView',
  components:{
    homePage,
    footerComponent,
    headerComponent,
  },
});
</script>