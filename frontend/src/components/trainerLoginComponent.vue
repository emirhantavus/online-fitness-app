<template>
  <div class="login-card trainer-login-card">
    <h2>Trainer Login</h2>
    <form @submit.prevent="loginTrainer">
      <div class="form-group">
        <label for="trainer-email">Email:</label>
        <input type="email" id="trainer-email" v-model="email" required>
      </div>
      <div class="form-group">
        <label for="trainer-password">Password:</label>
        <input type="password" id="trainer-password" v-model="password" required>
      </div>
      <button class="login-button" type="submit">Login</button>
    </form>
    <p>Don't have an account? <router-link to="/register">Click here to register</router-link></p>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

export default defineComponent({
  setup() {
    const email = ref('');
    const password = ref('');
    const errorMessage = ref('');
    const router = useRouter();

    const loginTrainer = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/trainer-login/', {
      email: email.value,
      password: password.value,
    });

    const isTrainer = response.data.is_trainer;
    const userId = response.data.user_id; // Varsayılan olarak bu bilgiyi de döndürdüğünüzü varsayıyorum.

    if (isTrainer) {
      // Save the token, user ID, and trainer status to local storage
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
      localStorage.setItem('user_id', userId.toString());
      localStorage.setItem('is_trainer', 'true'); // Trainer olarak işaretle

      router.push('/trainer-dashboard');
    } else {
      errorMessage.value = "Only trainers are allowed to login from this page.";
      setTimeout(() => {
        router.push('/login');
      }, 2000);
    }
  } catch (error: any) {
    console.error('Login failed:', error.response?.data);
    errorMessage.value = error.response?.data?.error || 'An error occurred during login.';
  }
};

    return {
      email,
      password,
      errorMessage,
      loginTrainer,
    };
  },
});
</script>

<style scoped>
.trainer-login-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 500px;
  width: 80%;
  margin: 0 auto; 
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  padding: 50px;
}

.trainer-login-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

.trainer-login-card h2 {
  margin-bottom: 20px;
  font-size: 28px;
  color: #333;
}

.form-group {
  margin-bottom: 25px;
  text-align: left;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

.form-group input {
  width: 300px;
  padding: 10px;
  border: 2px solid #ff9a9e;
  border-radius: 8px;
  transition: border-color 0.3s ease;
}

.form-group input:focus {
  border-color: #ff6a6a;
}

.login-button {
  background-color: #ff6a6a;
  color: #fff;
  border: none;
  padding: 10px 20px;
  font-size: 18px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 250px; 
  margin-top: 7px;
}

@media (max-width: 768px) {
  .trainer-login-card {
    padding: 30px;
  }

  .trainer-login-card h2 {
    font-size: 24px;
  }

  .form-group input {
    width: 100%;
    font-size: 14px;
    padding: 8px;
  }

  .login-button {
    font-size: 16px;
    padding: 8px 16px;
    width: 100%;
  }
}

@media (max-width: 480px) {
  .trainer-login-card {
    padding: 20px;
  }

  .trainer-login-card h2 {
    font-size: 20px;
  }

  .form-group input {
    width: 100%;
    font-size: 12px;
    padding: 6px;
  }

  .login-button {
    font-size: 14px;
    padding: 6px 12px;
    width: 100%;
  }
}
</style>

