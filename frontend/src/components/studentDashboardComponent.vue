<!-- views/student-dashboard.vue -->
<template>
  <div class="container">
    <h1>Student Dashboard</h1>
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else>
      <h2>Your Programs</h2>
      <ul>
        <li v-for="program in programs" :key="program.id" class="program-item">
          <div class="program-info">
            <h3>{{ program.title }}</h3>
            <p><strong>Start Date:</strong> {{ formatDate(program.start_date) }}</p>
            <p><strong>End Date:</strong> {{ formatDate(program.end_date) }}</p>
          </div>
          <button @click="viewProgram(program.id)">View Program</button>
        </li>
      </ul>
    </div>
    <ChatComponent />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import axios from '@/plugins/axios';

interface Program {
  id: number;
  title: string;
  start_date: string;
  end_date: string;
}

export default defineComponent({
  components: {
    
  },
  setup() {
    const loading = ref(true);
    const programs = ref<Program[]>([]);

    const fetchPrograms = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/programs/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        programs.value = response.data.results;
        loading.value = false;
      } catch (error) {
        console.error('Error fetching programs:', error);
      }
    };

    const viewProgram = (programId: number) => {
      window.location.href = `/student/programs/${programId}`;
    };

    const formatDate = (dateString: string) => {
      const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    };

    onMounted(() => {
      fetchPrograms();
    });

    return {
      loading,
      programs,
      fetchPrograms,
      viewProgram,
      formatDate
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
}
</style>
