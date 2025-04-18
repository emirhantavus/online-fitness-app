<template>
  <div class="wrapper">
    <PlanCard
      v-for="(plan, index) in plans"
      :key="plan.id"
      :plan="plan"
      :planClass="planClasses[index % planClasses.length]"
      @buyPlan="redirectToPayment(plan.id)"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import PlanCard from './planCard.vue';
import axios from '@/plugins/axios';

interface Feature {
  id: number;
  title: string;
}

interface Plan {
  id: number;
  title: string;
  price: number;
  features: Feature[];
}

export default defineComponent({
  name: 'PlanList',
  components: {
    PlanCard,
  },
  setup() {
    const plans = ref<Plan[]>([]);
    const planClasses = ref(['basic', 'Premium', 'Ultimate']);
    const router = useRouter();

    const fetchPlans = async () => {
      try {
        const response = await axios.get('/api/subplans/');
        plans.value = response.data;
      } catch (error) {
        console.error('Error fetching plans:', error);
      }
    };

    const redirectToPayment = (planId: number) => {
      const isLoggedIn = !!localStorage.getItem('access_token');
      if (isLoggedIn) {
        router.push({ name: 'Payment', params: { planId } });
      } else {
        router.push({ name: 'Register' });
      }
    };

    onMounted(fetchPlans);

    return {
      plans,
      planClasses,
      redirectToPayment,
    };
  },
});
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: #647df9;
  padding: 20px;
}

.wrapper {
  max-width: 1090px;
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  margin: auto;
  justify-content: space-between;
}

/* Responsive design for smaller screens */
@media (max-width: 768px) {
  .wrapper {
    flex-direction: column;
    align-items: center;
  }
}
</style>
