<template>
  <div>
    <h1>Trainer Program Details</h1>
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else>
      <div v-if="program">
        <div class="program-info">
          <h2>{{ program.title }}</h2>
          <p><strong>Trainer:</strong> {{ program.trainer.email }}</p>
          <p><strong>Student:</strong> {{ program.student.email }}</p>
          <p><strong>Start Date:</strong> {{ formatDate(program.start_date) }}</p>
          <p><strong>End Date:</strong> {{ formatDate(program.end_date) }}</p>
        </div>
        <div class="filter-buttons">
          <button v-for="day in days" :key="day" @click="selectedDay = day">
            {{ day }}
          </button>
          <button v-for="week in weeks" :key="week" @click="selectedWeek = week">
            Week {{ week }}
          </button>
        </div>
        <div class="exercises">
          <h3>Exercises for {{ selectedDay }} - Week {{ selectedWeek }}</h3>
          <ul>
            <li v-for="exercise in filteredExercises" :key="exercise.id" class="exercise-item">
              <h4>{{ exercise.title }}</h4>
              <p><strong>Sets/Reps:</strong> {{ exercise.sets_reps }}</p>
              <p><strong>Intensity:</strong> {{ exercise.intensity }}</p>
              <p><strong>Tempo:</strong> {{ exercise.tempo }}</p>
              <p><strong>Rest:</strong> {{ exercise.rest }}</p>
              <a :href="exercise.video_url" target="_blank">Watch Video</a>
              <textarea
                v-if="currentEvolution(exercise)"
                :value="currentEvolution(exercise)?.description"
                disabled
              ></textarea>
            </li>
          </ul>
        </div>
      </div>
      <div v-else>
        <p>No program found.</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from 'vue';
import apiClient from '@/plugins/axios';
import { useRoute } from 'vue-router';

interface UserProfile {
  bio: string;
  location: string;
  profile_pic: string | null;
  first_name: string;
  last_name: string;
}

interface Trainer {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  userprofile: UserProfile;
}

interface Student {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  userprofile: UserProfile;
}

interface Evolution {
  id: number;
  description: string;
  week_number: number;
}

interface Exercise {
  id: number;
  title: string;
  sets_reps: string;
  intensity: string;
  tempo: string;
  rest: string;
  video_url: string;
  day: string;
  evolutions: Evolution[];
}

interface Program {
  id: number;
  title: string;
  trainer: Trainer;
  student: Student;
  start_date: string;
  end_date: string;
  exercises: Exercise[];
}

export default defineComponent({
  setup() {
    const route = useRoute();
    const loading = ref(true);
    const program = ref<Program | null>(null);
    const selectedDay = ref('Monday');
    const selectedWeek = ref(1);

    const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    const weeks = [1, 2, 3, 4];

    const fetchProgramDetails = async () => {
      const programId = route.params.id;
      try {
        const response = await apiClient.get(`http://localhost:8000/api/programs/${programId}/`);
        program.value = response.data;
        loading.value = false;
      } catch (error) {
        console.error('Error fetching program details:', error);
      }
    };

    const filteredExercises = computed(() => {
      return program.value?.exercises.filter(exercise => exercise.day === selectedDay.value && exercise.evolutions.some(evolution => evolution.week_number === selectedWeek.value)) || [];
    });

    const currentEvolution = (exercise: Exercise) => {
      return exercise.evolutions.find(evo => evo.week_number === selectedWeek.value);
    };

    const formatDate = (dateString: string) => {
      const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    };

    onMounted(fetchProgramDetails);

    return {
      loading,
      program,
      selectedDay,
      selectedWeek,
      days,
      weeks,
      filteredExercises,
      currentEvolution,
      formatDate,
    };
  }
});
</script>

<style scoped>
h1 {
  margin-bottom: 20px;
  font-size: 32px;
  color: #4a90e2;
  text-align: center;
}

.loading {
  font-size: 18px;
  color: #333;
  text-align: center;
}

.program-info {
  width: 100%;
  text-align: center;
  margin-bottom: 20px;
}

.program-info h2 {
  margin: 0 0 10px;
  font-size: 24px;
  color: #333;
}

.program-info p {
  margin: 5px 0;
  font-size: 16px;
  color: #555;
}

.filter-buttons {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
}

.exercises {
  width: 100%;
}

.exercises h3 {
  margin: 20px 0 10px;
  font-size: 22px;
  color: #4a90e2;
  text-align: center;
}

.exercise-item {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 10px;
}

.exercise-item h4 {
  margin: 0 0 10px;
  font-size: 20px;
  color: #333;
}

.exercise-item p {
  margin: 5px 0;
  font-size: 16px;
  color: #555;
}

.exercise-item a {
  display: inline-block;
  margin-top: 10px;
  color: #4a90e2;
  text-decoration: underline;
}

.exercise-item a:hover {
  color: #357ab8;
}

textarea {
  width: 100%;
  padding: 5px;
  margin-top: 10px;
  font-size: 18px;
  resize: none;
  background-color: #f7f7f7;
  border: 1px solid #ddd;
  pointer-events: none;
}

button {
  margin-top: 10px;
  background-color: #4a90e2;
  color: #fff;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #357ab8;
}

@media (max-width: 600px) {
  h1 {
    font-size: 24px;
  }

  .program-info h2 {
    font-size: 20px;
  }

  .program-info p {
    font-size: 14px;
  }

  .filter-buttons button {
    font-size: 14px;
    padding: 8px;
  }

  .exercises h3 {
    font-size: 18px;
  }

  .exercise-item {
    padding: 15px;
  }

  .exercise-item h4 {
    font-size: 18px;
  }

  .exercise-item p {
    font-size: 14px;
  }

  .exercise-item a {
    font-size: 14px;
  }

  textarea {
    font-size: 14px;
  }

  button {
    font-size: 14px;
    padding: 8px 16px;
  }
}
</style>
