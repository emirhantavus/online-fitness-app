<template>
    <headerComponent/>
    <paymentComponent />
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import paymentComponent from '../components/paymentComponent.vue';
import headerComponent from '../components/headerComponent.vue';
import footerComponent from '../components/footerComponent.vue';
export default defineComponent({
  name: 'App',
  components: {
    paymentComponent,
    headerComponent,
    footerComponent,
  },
})
</script>

    