<template>
      <div class="container">
        <h1>Daily Calorie Calculator</h1>
        <form @submit.prevent="calculateCalories">
          <div class="form-group">
            <label for="age">Age:</label>
            <input v-model.number="form.age" type="number" id="age" required />
          </div>
          <div class="form-group">
            <label for="gender">Gender:</label>
            <select v-model="form.gender" id="gender" required>
              <option value="male">Male</option>
              <option value="female">Female</option>
            </select>
          </div>
          <div class="form-group">
            <label for="weight">Weight (kg):</label>
            <input v-model.number="form.weight" type="number" id="weight" required />
          </div>
          <div class="form-group">
            <label for="height">Height (cm):</label>
            <input v-model.number="form.height" type="number" id="height" required />
          </div>
          <div class="form-group">
            <label for="activity">Activity Level:</label>
            <select v-model="form.activity" id="activity" required>
              <option value="sedentary">Sedentary (little or no exercise)</option>
              <option value="light">Lightly active (light exercise/sports 1-3 days/week)</option>
              <option value="moderate">Moderately active (moderate exercise/sports 3-5 days/week)</option>
              <option value="active">Active (hard exercise/sports 6-7 days a week)</option>
              <option value="very_active">Very active (very hard exercise/sports & a physical job)</option>
            </select>
          </div>
          <button type="submit">Calculate</button>
        </form>
        <div v-if="result" class="result">
          <h2>Results</h2>
          <p><strong>Maintain weight:</strong> {{ result.maintain }} kcal/day</p>
          <p><strong>Weight loss:</strong> {{ result.loss }} kcal/day</p>
          <p><strong>Weight gain:</strong> {{ result.gain }} kcal/day</p>
        </div>
      </div>
    </template>
    
    <script lang="ts">
    import { defineComponent, ref } from 'vue';
    
    export default defineComponent({
      name: 'FitnessCalorieComponent',
      setup() {
        const form = ref({
          age: null as number | null,
          gender: 'male',
          weight: null as number | null,
          height: null as number | null,
          activity: 'sedentary',
        });
    
        const result = ref<null | { maintain: number; loss: number; gain: number }>(null);
    
        const activityFactors = {
          sedentary: 1.2,
          light: 1.375,
          moderate: 1.55,
          active: 1.725,
          very_active: 1.9,
        };
    
        const calculateCalories = () => {
          const age = form.value.age ?? 0;
          const gender = form.value.gender;
          const weight = form.value.weight ?? 0;
          const height = form.value.height ?? 0;
          const activity = form.value.activity;
    
          let bmr;
          if (gender === 'male') {
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age);
          } else {
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age);
          }
    
      const activityFactors: { [key: string]: number } = {
            sedentary: 1.2,
            light: 1.375,
            moderate: 1.55,
            active: 1.725,
            very_active: 1.9,
      };

      const tdee = bmr * activityFactors[activity];
    
          result.value = {
            maintain: Math.round(tdee),
            loss: Math.round(tdee - 500),
            gain: Math.round(tdee + 500),
          };
        };
    
        return {
          form,
          result,
          calculateCalories,
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
    
    .form-group input, .form-group select {
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
    