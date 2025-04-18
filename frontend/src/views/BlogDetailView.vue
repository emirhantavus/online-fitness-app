<template>
      <div>
        <headerComponent />
        <div class="main-content">
          <PostDetail />
        </div>
        <footerComponent />
      </div>
</template>
    
<script lang="ts">
import { defineComponent } from 'vue';
import PostDetail from '../components/postDetailComponent.vue';
import footerComponent from '../components/footerComponent.vue';
import headerComponent from '../components/headerComponent.vue';

export default defineComponent({
      name: 'planView',
      components: {
            PostDetail,
            footerComponent,
            headerComponent,
      }
})
</script>