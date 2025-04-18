<template>
      <div class="dashboard-container">
        <h2>User Dashboard</h2>
        <div class="cards-container">
          <div v-for="program in programs" :key="program.id" class="program-card">
            <h3>{{ program.name }}</h3>
            <p>{{ program.description }}</p>
            <p><strong>Trainer:</strong> {{ program.trainer }}</p>
            <p><strong>Duration:</strong> {{ program.duration }} weeks</p>
            <button @click="viewProgram(program.id)" class="view-button">View Program</button>
          </div>
        </div>
      </div>
</template>
    
<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'UserDashboard',
  setup() {
    const programs = ref([
      {
        id: 1,
        name: 'Beginner Workout',
        description: 'A basic workout program for beginners.',
        trainer: 'John Doe',
        duration: 6,
      },
      {
        id: 2,
        name: 'Intermediate Workout',
        description: 'An intermediate workout program to build on the basics.',
        trainer: 'Jane Smith',
        duration: 8,
      },
      {
        id: 3,
        name: 'Advanced Workout',
        description: 'An advanced workout program for experienced individuals.',
        trainer: 'Mike Johnson',
        duration: 12,
      },
    ]);

    const viewProgram = (programId: number) => {
      console.log('View program with ID:', programId);
      // Buraya program detay sayfasına yönlendirme kodunu ekleyebilirsiniz.
    };

    return {
      programs,
      viewProgram,
    };
  },
});
</script>

<style scoped>
.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 20px;
}

.cards-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.program-card {
  flex: 1 1 calc(33.333% - 20px);
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.program-card h3 {
  margin-bottom: 10px;
  color: #333;
  font-size: 20px;
}

.program-card p {
  margin-bottom: 10px;
  color: #666;
}

.view-button {
  padding: 10px 20px;
  background-color: #0056b3;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
}

.view-button:hover {
  background-color: #004494;
}
</style>
