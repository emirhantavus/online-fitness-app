<template>
  <div class="table" :class="planClass">
    <div class="price-section">
      <div class="price-area">
        <div class="inner-area">
          <span class="text">$</span>
          <span class="price">{{ plan.price }}</span>
        </div>
      </div>
    </div>
    <div class="package-name">{{ plan.title }}</div>
    <ul v-if="plan.features && plan.features.length" class="features">
      <li v-for="feature in plan.features" :key="feature.id">
        <span class="list-name">{{ feature.title }}</span>
        <span class="icon check"><i class="fas fa-check-circle"></i></span>
      </li>
    </ul>
    <p v-else>No features available</p>
    <div class="btn"><button @click="buyPlan">Buy this plan</button></div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import type { PropType } from 'vue';
import { useRouter } from 'vue-router';
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
  name: 'PlanCard',
  props: {
    plan: {
      type: Object as PropType<Plan>,
      required: true,
    },
    planClass: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const router = useRouter();

    const buyPlan = async () => {
      try {
        // Kullanıcı giriş yapmış mı kontrol et
        await axios.get('/api/profile/');  
        // Giriş yapmışsa ödeme sayfasına yönlendir
        router.push(`/payment?planId=${props.plan.id}`);
      } catch (error) {
        // Giriş yapmamışsa kayıt sayfasına yönlendir
        router.push('/register');
      }
    };

    return {
      buyPlan,
    };
  },
});
</script>

<style scoped>
.table {
  background: #fff;
  width: calc(33% - 20px);
  padding: 30px;
  position: relative;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
  margin: 10px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

@media (max-width: 1020px) {
  .table {
    width: calc(50% - 20px);
    margin-bottom: 40px;
  }
}

@media (max-width: 698px) {
  .table {
    width: 100%;
  }
}

.price-section {
  display: flex;
  justify-content: center;
}

.price-area {
  height: 120px;
  width: 120px;
  border-radius: 50%;
  padding: 2px;
}

.price-area .inner-area {
  height: 100%;
  width: 100%;
  border-radius: 50%;
  border: 3px solid #fff;
  color: #fff;
  line-height: 117px;
  text-align: center;
  position: relative;
}

.price-area .inner-area .text {
  font-size: 25px;
  font-weight: 400;
  position: absolute;
  top: -10px;
  left: 17px;
}

.price-area .inner-area .price {
  font-size: 55px;
  font-weight: 500;
}

.package-name {
  width: 100%;
  height: 2px;
  background: #ffecb3;
  margin: 35px 0;
  position: relative;
  text-align: center;
  font-size: 25px;
  font-weight: bolder;
}

.features {
  list-style: none;
  padding: 0;
  margin: 0;
}

.features li {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}

.features .list-name {
  font-size: 17px;
  font-weight: 400;
}

.features .icon {
  font-size: 15px;
}

.features .icon.check {
  color: #2db94d;
}

.features .icon.cross {
  color: #cd3241;
}

.btn {
  display: flex;
  justify-content: center;
  margin-top: 35px;
}

.btn button {
  width: 80%;
  height: 50px;
  font-weight: 700;
  color: #fff;
  font-size: 20px;
  border: none;
  outline: none;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.basic .price-area,
.basic .inner-area {
  background: #ffd861;
}

.basic .btn button {
  background: #ffd861;
}

.basic .btn button:hover {
  border-radius: 6px;
  background: #fff;
  color: #ffd861;
  border: 2px solid #ffd861;
}

.Premium .price-area,
.Premium .inner-area {
  background: #a26bfa;
}

.Premium .btn button {
  background: #a26bfa;
}

.Premium .btn button:hover {
  border-radius: 6px;
  background: #fff;
  color: #a26bfa;
  border: 2px solid #a26bfa;
}

.Ultimate .price-area,
.Ultimate .inner-area {
  background: #43ef8b;
}

.Ultimate .btn button {
  background: #43ef8b;
}

.Ultimate .btn button:hover {
  border-radius: 6px;
  background: #fff;
  color: #43ef8b;
  border: 2px solid #43ef8b;
}
</style>
