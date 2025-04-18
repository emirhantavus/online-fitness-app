<template>
      <div>
        <headerComponent />
        <div class="main-content">
          <message />
        </div>
        <footerComponent />
      </div>
</template>
    
<script lang="ts">
import { defineComponent } from 'vue';
import message from '../components/messagesComponent.vue';
import footerComponent from '../components/footerComponent.vue';
import headerComponent from '../components/headerComponent.vue';

export default defineComponent({
      name: 'planView',
      components: {
            message,
            footerComponent,
            headerComponent,
      }
})
</script>