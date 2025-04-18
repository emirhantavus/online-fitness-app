<template>
  <div class="container">
    <h1>1RM Calculator</h1>
    <form @submit.prevent="calculate1RM">
      <div class="form-group">
        <label for="weight">Weight Lifted (kg):</label>
        <input v-model.number="form.weight" type="number" id="weight" required />
      </div>
      <div class="form-group">
        <label for="reps">Repetitions:</label>
        <input v-model.number="form.reps" type="number" id="reps" required />
      </div>
      <button type="submit">Calculate 1RM</button>
    </form>
    <div v-if="result !== null" class="result">
      <h2>Result</h2>
      <p><strong>1RM:</strong> {{ result }} kg</p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'OneRMCalculator',
  setup() {
    const form = ref({
      weight: null as number | null,
      reps: null as number | null,
    });

    const result = ref<number | null>(null);

    const calculate1RM = () => {
      const weight = form.value.weight ?? 0;
      const reps = form.value.reps ?? 0;
      result.value = Math.round(weight * (1 + reps / 30));
    };

    return {
      form,
      result,
      calculate1RM,
    };
  },
});
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px;
  background-color: #f7f7f7;
  border-radius: 8px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  margin: 50px auto;
}

h1 {
  margin-bottom: 20px;
  font-size: 32px;
  color: #ff6a6a;
}

form {
  width: 100%;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 2px solid #ff9a9e;
  border-radius: 8px;
  font-size: 16px;
}

button {
  background-color: #ff6a6a;
  color: #fff;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 100%;
}

button:hover {
  background-color: #e65c5c;
}

.result {
  margin-top: 20px;
  width: 100%;
}

.result h2 {
  margin-bottom: 10px;
  font-size: 24px;
  color: #ff6a6a;
}

.result p {
  font-size: 18px;
  color: #333;
  margin: 5px 0;
}
</style>
