<template>
  <div class="container">
    <h1>Nutrition Search</h1>
    <div class="search-bar">
      <input v-model="query" type="text" placeholder="Enter food item" />
      <button @click="fetchNutritionData">Search</button>
    </div>
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else>
      <div v-if="nutritionData" class="nutrition-info">
        <div class="primary-info">
          <div class="info-item"><strong>Calories:</strong> {{ nutritionData.calories }}</div>
          <div class="info-item"><strong>Protein:</strong> {{ nutritionData.protein_g }} g</div>
          <div class="info-item"><strong>Carbohydrates:</strong> {{ nutritionData.carbohydrates_total_g }} g</div>
          <div class="info-item"><strong>Total Fat:</strong> {{ nutritionData.fat_total_g }} g</div>
        </div>
        <div class="secondary-info">
          <div class="info-item"><strong>Serving Size:</strong> {{ nutritionData.serving_size_g }} g</div>
          <div class="info-item"><strong>Saturated Fat:</strong> {{ nutritionData.fat_saturated_g }} g</div>
          <div class="info-item"><strong>Sodium:</strong> {{ nutritionData.sodium_mg }} mg</div>
          <div class="info-item"><strong>Potassium:</strong> {{ nutritionData.potassium_mg }} mg</div>
          <div class="info-item"><strong>Cholesterol:</strong> {{ nutritionData.cholesterol_mg }} mg</div>
          <div class="info-item"><strong>Fiber:</strong> {{ nutritionData.fiber_g }} g</div>
          <div class="info-item"><strong>Sugar:</strong> {{ nutritionData.sugar_g }} g</div>
        </div>
      </div>
      <div v-else-if="error" class="error">{{ error }}</div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import axios from 'axios';

export default defineComponent({
  name: 'FoodCalorieComponent',
  setup() {
    const query = ref('');
    const nutritionData = ref<any>(null);
    const loading = ref(false);
    const error = ref('');

    const fetchNutritionData = async () => {
      if (!query.value) {
        return;
      }

      loading.value = true;
      error.value = '';
      nutritionData.value = null;

      try {
        const response = await axios.get(`http://localhost:8000/api/nutrition/?query=${query.value}`);
        if (response.status === 200 && response.data.length > 0) {
          nutritionData.value = response.data[0];
        } else {
          error.value = 'Food not found.';
        }
      } catch (err) {
        error.value = 'Error fetching nutrition data.';
      } finally {
        loading.value = false;
      }
    };

    return {
      query,
      nutritionData,
      loading,
      error,
      fetchNutritionData,
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

.search-bar {
  display: flex;
  justify-content: center;
  width: 100%;
  margin-bottom: 20px;
}

input {
  flex: 1;
  padding: 10px;
  border: 2px solid #ff9a9e;
  border-radius: 8px 0 0 8px;
  font-size: 16px;
}

button {
  background-color: #ff6a6a;
  color: #fff;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  border-radius: 0 8px 8px 0;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #e65c5c;
}

.loading {
  font-size: 18px;
  color: #555;
}

.nutrition-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 100%;
}

.primary-info, .secondary-info {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  width: 100%;
  margin-bottom: 20px;
}

.info-item {
  margin-bottom: 10px;
  background: #fff;
  padding: 10px;
  border-radius: 4px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  width: 48%;
}

.info-item strong {
  color: #ff6a6a;
}

.error {
  color: #e65c5c;
  font-size: 18px;
  margin-top: 20px;
}

/* Responsive Styles */
@media (max-width: 768px) {
  .info-item {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 20px;
  }

  .search-bar {
    flex-direction: column;
    align-items: stretch;
  }

  input, button {
    width: 100%;
    border-radius: 8px;
    margin-bottom: 10px;
  }

  button {
    border-radius: 8px;
  }
}
</style>
