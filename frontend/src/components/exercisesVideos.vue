<template>
  <div class="exercises">
    <h1>Exercise Videos Page</h1>
    <div class="search-container">
      <input type="text" v-model="searchQuery" @input="handleSearchInput" placeholder="Search exercises..." class="search-input" />
    </div>
    <div class="exercise-cards">
      <div class="exercise-card" v-for="exercise in filteredExercises" :key="exercise.id">
        <img src="@/assets/video_logo.png" alt="Exercise Logo" class="exercise-logo" />
        <h2>{{ exercise.title }}</h2>
        <button class="view-details-button" @click="viewDetails(exercise.slug)">Click to View</button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

interface ExerciseVideo {
  id: number;
  title: string;
  slug: string;
  video_url: string;
}

export default defineComponent({
  name: 'ExerciseVideos',
  setup() {
    const exercises = ref<ExerciseVideo[]>([]);
    const searchQuery = ref<string>('');
    const router = useRouter();

    const fetchExercises = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/videos/');
        exercises.value = response.data.results;
      } catch (error) {
        console.error('Error fetching exercises:', error);
      }
    };

    onMounted(() => {
      fetchExercises();
    });

    const filteredExercises = computed(() => {
      return exercises.value.filter(exercise => {
        return exercise.title.toLowerCase().includes(searchQuery.value.toLowerCase());
      });
    });

    const handleSearchInput = () => {
      fetchExercises();
    };

    const viewDetails = (slug: string) => {
      console.log('Navigating to:', slug);
      if (slug) {
        router.push(`/exercises/${slug}`).catch(err => {
          console.error('Error during navigation:', err);
        });
      } else {
        console.error('Slug is undefined');
      }
    };

    return {
      exercises,
      searchQuery,
      filteredExercises,
      handleSearchInput,
      viewDetails
    };
  }
});
</script>

<style scoped>
.exercises {
  padding: 20px;
}

.search-container {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
}

.search-input {
  width: 60%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.exercise-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.exercise-card {
  width: 200px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #fff;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.exercise-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.exercise-logo {
  width: 70px;
  height: 70px;
  margin-bottom: 10px;
}

.view-details-button {
  margin-top: auto;
  background-color: #4CAF50;
  border: none;
  color: white;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.view-details-button:hover {
  background-color: #45a049;
}

/* Responsive styles */
@media (max-width: 768px) {
  .exercise-card {
    width: 100%;
  }

  .search-input {
    width: 80%;
  }
}

@media (max-width: 480px) {
  .exercise-card {
    width: 100%;
  }

  .search-input {
    width: 100%;
  }
}
</style>
