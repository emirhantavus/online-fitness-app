<template>
  <div class="payment-container">
    <h1>Payment</h1>
    <form @submit.prevent="makePayment">
      <div class="form-group">
        <label for="name">Name and Surname</label>
        <input id="name" v-model="name" required />
      </div>
      <div class="form-group">
        <label for="cardNumber">Card Number</label>
        <input id="cardNumber" v-model="formattedCardNumber" @input="formatCardNumber" maxlength="19" required />
      </div>
      <div class="form-group">
        <label for="expiryDate">Expiry Date</label>
        <input id="expiryDate" v-model="expiryDate" placeholder="MM/YY" maxlength="5" required />
      </div>
      <div class="form-group">
        <label for="cvv">CVV</label>
        <input id="cvv" v-model="cvv" maxlength="4" required />
      </div>
      <div class="form-group">
        <label for="securityCode">Security Code</label>
        <input id="securityCode" v-model="securityCode" required />
      </div>
      <button type="submit">Pay</button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from '@/plugins/axios';

export default defineComponent({
  name: 'Payment',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const name = ref('');
    const cardNumber = ref('');
    const formattedCardNumber = ref('');
    const expiryDate = ref('');
    const cvv = ref('');
    const securityCode = ref('');
    const planId = ref(route.query.planId as string);

    const formatCardNumber = (event: Event) => {
      const input = event.target as HTMLInputElement;
      const rawCardNumber = input.value.replace(/\D/g, '').substring(0, 16);
      cardNumber.value = rawCardNumber;
      formattedCardNumber.value = rawCardNumber.replace(/(\d{4})(?=\d)/g, '$1-').trim();
    };

    const makePayment = async () => {
      try {
        const response = await axios.post(`/api/subplans/purchase/`, { subplan_id: planId.value });
        alert('Payment successful');
        router.push('/student-dashboard');
      } catch (error:any) {
        if (error.response && error.response.data.error === "You already have an active subscription.") {
          alert("You already have an active subscription.");
          router.push('/student-dashboard')
        } else {
          console.error('Payment failed', error);
          alert('Payment failed');
        }
      }
    };

    return {
      name,
      cardNumber,
      formattedCardNumber,
      expiryDate,
      cvv,
      securityCode,
      makePayment,
      formatCardNumber,
    };
  },
});
</script>

<style scoped>
.payment-container {
  max-width: 500px;
  margin: 20px auto;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.payment-container h1 {
  text-align: center;
  margin-bottom: 20px;
}

.payment-container form {
  display: flex;
  flex-direction: column;
}

.payment-container .form-group {
  margin-bottom: 15px;
}

.payment-container label {
  display: block;
  margin-bottom: 5px;
}

.payment-container input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

.payment-container button {
  background: #4a90e2;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.payment-container button:hover {
  background: #357ab8;
}

/* Responsive styles */
@media (max-width: 768px) {
  .payment-container {
    padding: 10px;
  }

  .payment-container h1 {
    font-size: 24px;
  }

  .payment-container input {
    padding: 6px;
  }

  .payment-container button {
    padding: 8px;
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .payment-container {
    padding: 8px;
  }

  .payment-container h1 {
    font-size: 20px;
  }

  .payment-container input {
    padding: 5px;
  }

  .payment-container button {
    padding: 6px;
    font-size: 12px;
  }
}
</style>
