<!-- views/trainer-dashboard.vue -->
<template>
  <div class="container">
    <h1>Trainer Dashboard</h1>
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else>
      <h2>Your Students</h2>
      <ul>
        <li v-for="program in programs" :key="program.id" class="program-item">
          <div class="program-info">
            <h3>{{ program.student.email }}</h3>
            <p><strong>Program Title:</strong> {{ program.title }}</p>
            <p><strong>Start Date:</strong> {{ formatDate(program.start_date) }}</p>
            <p><strong>End Date:</strong> {{ formatDate(program.end_date) }}</p>
          </div>
          <button @click="toggleEditForm(program)">{{ program.showEditForm ? 'Cancel' : 'Edit Program' }}</button>
          <button @click="viewStudentProgram(program.id)">View Program</button>
          <div v-if="program.showEditForm" class="program-form">
            <div class="exercise-section">
              <h3>Add Exercise</h3>
              <label>Week:</label>
              <select v-model="selectedWeek">
                <option v-for="week in weeks" :key="week" :value="week">{{ week }}</option>
              </select>
              <label>Day:</label>
              <select v-model="selectedDay">
                <option v-for="day in days" :key="day" :value="day">{{ day }}</option>
              </select>
              <label>Exercise Title:</label>
              <input v-model="newExercise.title" placeholder="Exercise Title" />
              <label>Sets/Reps:</label>
              <input v-model="newExercise.sets_reps" placeholder="Sets/Reps" />
              <label>Intensity:</label>
              <input v-model="newExercise.intensity" placeholder="Intensity" />
              <label>Tempo:</label>
              <input v-model="newExercise.tempo" placeholder="Tempo" />
              <label>Rest:</label>
              <input v-model="newExercise.rest" placeholder="Rest" />
              <label>Video URL:</label>
              <input v-model="newExercise.video_url" placeholder="Video URL" />
              <button @click="addExercise(program)">Add Exercise</button>
            </div>
          </div>
        </li>
      </ul>
    </div>
    <ChatComponent />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import axios from '@/plugins/axios';

interface UserProfile {
  bio: string;
  location: string;
  profile_pic: string | null;
  first_name: string;
  last_name: string;
}

interface Student {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  userprofile: UserProfile;
}

interface Exercise {
  id?: number;
  title: string;
  sets_reps: string;
  intensity: string;
  tempo: string;
  rest: string;
  video_url: string;
  week?: number;
  day?: string;
}

interface Program {
  id: number;
  title: string;
  student: Student;
  start_date: string;
  end_date: string;
  exercises: Record<number, Record<string, Exercise[]>>;
  showEditForm?: boolean;
}

export default defineComponent({
  components: {
    
  },
  setup() {
    const loading = ref(true);
    const programs = ref<Program[]>([]);
    const selectedWeek = ref<number>(1);
    const selectedDay = ref<string>('Monday');
    const newExercise = ref<Exercise>({
      title: '',
      sets_reps: '',
      intensity: '',
      tempo: '',
      rest: '',
      video_url: ''
    });

    const weeks = [1, 2, 3, 4];
    const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

    const fetchPrograms = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/programs/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        programs.value = response.data.results.map((program: Program) => ({
          ...program,
          showEditForm: false,
          exercises: program.exercises || {}
        }));
        loading.value = false;
      } catch (error) {
        console.error('Error fetching programs:', error);
      }
    };

    const addExercise = async (program: Program) => {
      try {
        const exerciseToSend = {
          ...newExercise.value,
          week: selectedWeek.value,
          day: selectedDay.value
        };

        await axios.post(
          `http://localhost:8000/api/exercise-programs/`,
          {
            program_id: program.id,
            ...exerciseToSend
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('access_token')}`
            }
          }
        );
        alert('Exercise added successfully');
        fetchPrograms();
        newExercise.value = {
          title: '',
          sets_reps: '',
          intensity: '',
          tempo: '',
          rest: '',
          video_url: ''
        };
      } catch (error) {
        console.error('Error adding exercise:', error);
      }
    };

    const viewStudentProgram = (programId: number) => {
      window.location.href = `/trainer/programs/${programId}`;
    };

    const formatDate = (dateString: string) => {
      const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    };

    const toggleEditForm = (program: Program) => {
      program.showEditForm = !program.showEditForm;
      if (program.showEditForm) {
        selectedWeek.value = 1;
        selectedDay.value = 'Monday';
        newExercise.value = {
          title: '',
          sets_reps: '',
          intensity: '',
          tempo: '',
          rest: '',
          video_url: ''
        };
      }
    };

    onMounted(() => {
      fetchPrograms();
    });

    return {
      loading,
      programs,
      selectedWeek,
      selectedDay,
      newExercise,
      weeks,
      days,
      fetchPrograms,
      addExercise,
      viewStudentProgram,
      formatDate,
      toggleEditForm
    };
  }
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
  max-width: 800px;
  margin: 50px auto;
  width: 90%;
}

h1 {
  margin-bottom: 20px;
  font-size: 32px;
  color: #4a90e2;
  text-align: center;
}

.loading {
  font-size: 18px;
  color: #333;
}

ul {
  list-style: none;
  padding: 0;
}

.program-item {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 10px;
  width: 100%;
}

.program-info {
  text-align: left;
  margin-bottom: 20px;
}

.program-info h3 {
  margin: 0 0 10px;
  font-size: 24px;
  color: #333;
}

.program-info p {
  margin: 5px 0;
  font-size: 16px;
  color: #555;
}

button {
  background-color: #4a90e2;
  color: #fff;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-bottom: 10px;
}

button:hover {
  background-color: #357ab8;
}

.program-form {
  margin-top: 20px;
  width: 100%;
}

.program-form h2 {
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
}

.program-form label {
  display: block;
  margin-bottom: 10px;
  font-size: 16px;
  color: #555;
}

.program-form input,
.program-form select {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  font-size: 14px;
}

.exercise-section {
  margin-bottom: 20px;
}

.exercise-section h3 {
  font-size: 20px;
  color: #4a90e2;
}

.exercise-section label {
  font-size: 14px;
  color: #555;
}

.exercise-section input,
.exercise-section select {
  margin-bottom: 10px;
}

.exercise-section button {
  display: block;
  width: 100%;
  margin-top: 10px;
}

@media (max-width: 768px) {
  .container {
    padding: 20px;
  }

  h1 {
    font-size: 24px;
  }

  .program-info h3 {
    font-size: 20px;
  }

  .program-info p {
    font-size: 14px;
  }

  button {
    font-size: 14px;
    padding: 8px 16px;
  }

  .program-form h2 {
    font-size: 20px;
  }

  .program-form label {
    font-size: 14px;
  }

  .program-form input,
  .program-form select {
    font-size: 12px;
    padding: 8px;
  }

  .exercise-section h3 {
    font-size: 18px;
  }

  .exercise-section label {
    font-size: 12px;
  }

  .exercise-section input,
  .exercise-section select {
    font-size: 12px;
    padding: 8px;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 10px;
  }

  h1 {
    font-size: 20px;
  }

  .program-info h3 {
    font-size: 18px;
  }

  .program-info p {
    font-size: 12px;
  }

  button {
    font-size: 12px;
    padding: 6px 12px;
  }

  .program-form h2 {
    font-size: 18px;
  }

  .program-form label {
    font-size: 12px;
  }

  .program-form input,
  .program-form select {
    font-size: 10px;
    padding: 6px;
  }

  .exercise-section h3 {
    font-size: 16px;
  }

  .exercise-section label {
    font-size: 10px;
  }

  .exercise-section input,
  .exercise-section select {
    font-size: 10px;
    padding: 6px;
  }
}
</style>
