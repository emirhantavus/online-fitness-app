<template>
      <div>
        <headerComponent />
        <div class="main-content">
          <blogList />
        </div>
        <footerComponent />
      </div>
</template>
    
<script lang="ts">
import { defineComponent } from 'vue';
import blogList from '../components/blogListComponent.vue';
import footerComponent from '../components/footerComponent.vue';
import headerComponent from '../components/headerComponent.vue';

export default defineComponent({
      name: 'planView',
      components: {
            blogList,
            footerComponent,
            headerComponent,
      }
})
</script>