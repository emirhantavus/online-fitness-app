<template>
  <div id="app">
    <sideMenuComponent />
    <router-view />
  </div>
</template>

<script setup lang="ts">
import sideMenuComponent from './components/sideMenuComponent.vue';
</script>

<style>
/* Global CSS Reset */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  margin: 0;
  padding: 0;
  height: 100%;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #003467;
  height: 100%;
}
</style>
