<template>
  <div class="trainers-container">
    <h1>Our Trainers</h1>
    <div v-if="isMobile">
      <div class="trainer-card" v-for="trainer in trainers" :key="trainer.id" @click="goToProfile(trainer.id)">
        <img v-if="trainer.userprofile && trainer.userprofile.profile_pic" :src="getImage(trainer.userprofile.profile_pic)" alt="Trainer profile pic" class="trainer-image">
        <div class="trainer-details">
          <h2>{{ trainer.first_name }} {{ trainer.last_name }}</h2>
          <p>Email: {{ trainer.email }}</p>
          <p>Monthly Salary: ${{ trainer.monthly_rate }}</p>
          <button @click.stop="buyPlan(trainer.id)">Buy this plan</button>
        </div>
      </div>
    </div>
    <table v-else class="trainer-table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Email</th>
          <th>Monthly Salary</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="trainer in trainers" :key="trainer.id" @click="goToProfile(trainer.id)">
          <td>
            <img v-if="trainer.userprofile && trainer.userprofile.profile_pic" :src="getImage(trainer.userprofile.profile_pic)" alt="Trainer profile pic" class="trainer-image">
            {{ trainer.first_name }} {{ trainer.last_name }}
          </td>
          <td>{{ trainer.email }}</td>
          <td>${{ trainer.monthly_rate }}</td>
          <td><button @click.stop="buyPlan(trainer.id)">Buy this plan</button></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import apiClient from '@/plugins/axios';

interface UserProfile {
  profile_pic: string | null;
  bio: string;
  location: string;
}

interface Trainer {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  monthly_rate: string;
  userprofile?: UserProfile;
}

export default defineComponent({
  name: 'TrainersList',
  setup() {
    const trainers = ref<Trainer[]>([]);
    const isMobile = ref(window.innerWidth <= 768);
    const router = useRouter();

    const handleResize = () => {
      isMobile.value = window.innerWidth <= 768;
    };

    window.addEventListener('resize', handleResize);

    onMounted(async () => {
      try {
        const response = await apiClient.get('/api/trainers/');
        trainers.value = response.data.results;
      } catch (error) {
        console.error('Error fetching trainers:', error);
      }
    });

    const getImage = (imagePath: string) => {
      return `${imagePath}`;
    };

    const buyPlan = async (trainerId: number) => {
      try {
        await apiClient.get('/api/profile/');
        router.push(`/trainer-payment?trainerId=${trainerId}`);
      } catch (error) {
        router.push('/register');
      }
    };

    const goToProfile = (trainerId: number) => {
      router.push(`/trainer-profile/${trainerId}`);
    };

    return { trainers, getImage, buyPlan, goToProfile, isMobile };
  }
});
</script>

<style scoped>
.trainers-container {
  padding: 40px;
  max-width: 1200px;
  margin: 50px auto;
}

h1 {
  font-size: 36px;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.trainer-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.trainer-table th, .trainer-table td {
  padding: 12px;
  border-bottom: 1px solid #ddd;
  font-size: 20px;
}

.trainer-table th {
  background-color: #f2f2f2;
}

.trainer-table tr:hover {
  background-color: #f1f1f1;
  cursor: pointer;
}

.trainer-image {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 10px;
  vertical-align: middle;
}

.trainer-card {
  display: none;
  align-items: center;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.trainer-details {
  flex: 1;
}

.trainer-details h2 {
  margin: 0 0 10px;
}

.trainer-details p {
  margin: 5px 0;
}

button {
  background: #4a90e2;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-size: 16px;
}

button:hover {
  background: #357ab8;
}

@media (max-width: 768px) {
  .trainer-table {
    display: none;
  }

  .trainer-card {
    display: flex;
  }

  .trainer-image {
    width: 80px;
    height: 80px;
    margin-bottom: 10px;
  }

  button {
    font-size: 14px;
    padding: 8px 16px;
  }
}

@media (max-width: 480px) {
  .trainers-container {
    padding: 10px;
  }

  h1 {
    font-size: 24px;
  }

  .trainer-card {
    padding: 10px;
  }

  .trainer-image {
    width: 60px;
    height: 60px;
  }

  button {
    font-size: 12px;
    padding: 6px 12px;
  }
}
</style>
