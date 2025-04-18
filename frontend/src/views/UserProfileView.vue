<template>
      <div class="main-content">
            <headerComponent />
            <userProfileComponent />
      </div>
</template>
    
<script lang="ts">
import { defineComponent } from 'vue';
import userProfileComponent from '../components/userProfileComponent.vue';
import headerComponent from '../components/headerComponent.vue';

export default defineComponent({
      name: 'userProfile',
      components: {
        userProfileComponent,
        headerComponent,
      }
})
</script>