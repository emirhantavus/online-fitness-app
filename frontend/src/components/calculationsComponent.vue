<template>
      <div>
        <div class="calculations-container">
          <h1>Fitness Calculations</h1>
          <div class="card-grid">
            <div class="card" @click="goToCalculation('food-calorie-calculation')">
              <h2>Calorie Calculator</h2>
              <p>Calculate your daily calorie intake based on your goals.</p>
            </div>
            <div class="card" @click="goToCalculation('body-fat-calculation')">
              <h2>Body Fat Calculator</h2>
              <p>Calculate your body fat percentage based on various inputs.</p>
            </div>
            <div class="card" @click="goToCalculation('daily-calorie-needs')">
              <h2>Daily Calorie Needs</h2>
              <p>Find out your daily calorie needs based on your activity level.</p>
            </div>
            <div class="card" @click="goToCalculation('one-rep-max')">
              <h2>One Rep Max Calculator</h2>
              <p>Find out your one-rep max for different exercises.</p>
            </div>
            <!-- Diğer hesaplama kartlarını buraya ekleyebilirsiniz -->
          </div>
        </div>
        <footerComponent />
      </div>
    </template>
    
    <script lang="ts">
    import { defineComponent } from 'vue';
    import { useRouter } from 'vue-router';
    
    export default defineComponent({
      name: 'CalculationsView',
      setup() {
        const router = useRouter();
    
        const goToCalculation = (calculationType: string) => {
          router.push(`/calculations/${calculationType}`);
        };
    
        return {
          goToCalculation,
        };
      },
    });
    </script>
    
    <style scoped>
    .calculations-container {
      padding: 40px;
      max-width: 1200px;
      margin: 50px auto;
      background-color: #f9f9f9;
      border-radius: 10px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
      text-align: center;
    }
    
    h1 {
      font-size: 32px;
      color: #333;
      margin-bottom: 20px;
    }
    
    .card-grid {
      display: flex;
      flex-wrap: wrap;
      gap: 20px;
      justify-content: center;
    }
    
    .card {
      background: #fff;
      border-radius: 8px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
      cursor: pointer;
      transition: transform 0.3s ease, box-shadow 0.3s ease;
      overflow: hidden;
      width: 250px;
      padding: 20px;
      text-align: center;
    }
    
    .card:hover {
      transform: translateY(-5px);
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .card h2 {
      font-size: 24px;
      color: #ff6a6a;
      margin-bottom: 10px;
    }
    
    .card p {
      font-size: 16px;
      color: #777;
    }
    </style>
    