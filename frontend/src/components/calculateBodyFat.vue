<template>
  <div class="register-card">
    <h2>Body Fat Calculator</h2>
    <form @submit.prevent="calculateBodyFat">
      <div class="form-group">
        <label for="gender">Gender:</label>
        <div class="radio-group">
          <input type="radio" id="male" v-model="gender" value="male" required>
          <label for="male">Male</label>
          <input type="radio" id="female" v-model="gender" value="female" required>
          <label for="female">Female</label>
        </div>
      </div>
      <div class="form-group">
        <label for="height">Height (cm):</label>
        <input type="number" v-model.number="height" id="height" required min="0" max="250">
      </div>
      <div class="form-group">
        <label for="neck">Neck Circumference (cm):</label>
        <input type="number" v-model.number="neck" id="neck" required min="0">
      </div>
      <div class="form-group">
        <label for="waist">Waist Circumference (cm) (at the narrowest point):</label>
        <input type="number" v-model.number="waist" id="waist" required min="0">
      </div>
      <button type="submit" class="register-button">Calculate</button>
    </form>
    <div v-if="bodyFatPercentage !== null" class="calculation-info">
      <h3>Your Body Fat Percentage: {{ bodyFatPercentage.toFixed(2) }}%</h3>
      <h3>{{ bodyFatCategory }}</h3>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';

export default defineComponent({
  name: 'BodyFatCalculator',
  setup() {
    const gender = ref<string>('male');
    const height = ref<number | null>(null);
    const neck = ref<number | null>(null);
    const waist = ref<number | null>(null);
    const bodyFatPercentage = ref<number | null>(null);

    const calculateBodyFat = () => {
      if (height.value !== null && neck.value !== null && waist.value !== null) {
        if (gender.value === 'male') {
          bodyFatPercentage.value = 495 / (1.0324 - 0.19077 * Math.log10(waist.value - neck.value) + 0.15456 * Math.log10(height.value)) - 450;
        } else {
          bodyFatPercentage.value = 495 / (1.29579 - 0.35004 * Math.log10(waist.value + neck.value) + 0.22100 * Math.log10(height.value)) - 450;
        }
        if (bodyFatPercentage.value < 0) {
          bodyFatPercentage.value = null;
          alert('Please enter valid values.');
        }
      }
    };

    const bodyFatCategory = computed(() => {
      if (bodyFatPercentage.value !== null) {
        if (gender.value === 'male') {
          if (bodyFatPercentage.value < 6) return 'Essential Fat';
          if (bodyFatPercentage.value < 24) return 'Athletes';
          if (bodyFatPercentage.value < 31) return 'Fitness';
          return 'Obese';
        } else {
          if (bodyFatPercentage.value < 14) return 'Essential Fat';
          if (bodyFatPercentage.value < 21) return 'Athletes';
          if (bodyFatPercentage.value < 32) return 'Fitness';
          return 'Obese';
        }
      }
      return '';
    });

    return {
      gender,
      height,
      neck,
      waist,
      bodyFatPercentage,
      calculateBodyFat,
      bodyFatCategory
    };
  }
});
</script>

<style scoped>
.register-card {
  max-width: 600px;
  margin: 0 auto;
  padding: 40px;
  flex: 1;
  text-align: center;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #f9f9f9;
}

.register-card h2 {
  margin-bottom: 20px;
  font-size: 28px;
  color: #333;
}

.form-group {
  margin-bottom: 20px;
  text-align: left;
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
  transition: border-color 0.3s ease;
}

.form-group input:focus {
  border-color: #ff6a6a;
}

.register-button {
  background-color: #ff6a6a;
  color: #fff;
  border: none;
  padding: 12px 20px;
  font-size: 18px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 100%;
  margin-top: 20px;
}

.register-button:hover {
  background-color: #e65c5c;
}

.calculation-info {
  margin-top: 30px;
}

.calculation-info h3 {
  text-align: center;
  color: #4CAF50;
  margin-top: 20px;
}

/* Responsive styles */
@media (max-width: 768px) {
  .register-card {
    padding: 20px;
  }

  .form-group input {
    padding: 8px;
  }

  .register-button {
    padding: 10px;
    font-size: 16px;
  }

  .register-card h2 {
    font-size: 24px;
  }
}

@media (max-width: 480px) {
  .register-card {
    padding: 10px;
  }

  .form-group input {
    padding: 6px;
  }

  .register-button {
    padding: 8px;
    font-size: 14px;
  }

  .register-card h2 {
    font-size: 20px;
  }
}
</style>
