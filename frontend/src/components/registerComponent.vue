<template>
  <div class="register-card">
    <h2>Register</h2>
    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <label for="first-name">First Name</label>
        <input type="text" id="first-name" v-model="form.first_name" required />
      </div>
      <div class="form-group">
        <label for="last-name">Last Name</label>
        <input type="text" id="last-name" v-model="form.last_name" required />
      </div>
      <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" v-model="form.email" required />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" v-model="form.password" required />
      </div>
      <div class="form-group">
        <label for="confirmPassword">Confirm Password</label>
        <input type="password" id="confirmPassword" v-model="form.confirmPassword" required />
      </div>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      <button type="submit" class="register-button">Register</button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'RegisterForm',
  setup() {
    const form = ref({
      first_name: '',
      last_name: '',
      email: '',
      password: '',
      confirmPassword: '',
    });
    const errorMessage = ref('');
    const router = useRouter();

    const handleRegister = async () => {
      if (form.value.password !== form.value.confirmPassword) {
        errorMessage.value = 'Passwords do not match.';
        return;
      }

      try {
        const response = await axios.post('http://localhost:8000/api/register/', {
          first_name: form.value.first_name,
          last_name: form.value.last_name,
          email: form.value.email,
          password: form.value.password,
        });

        if (response.data.access && response.data.refresh && response.data.user && response.data.user.id) {
          localStorage.setItem('access_token', response.data.access);
          localStorage.setItem('refresh_token', response.data.refresh);
          localStorage.setItem('user_id', response.data.user.id);
          console.log('User registered:', response.data);
          router.push('/login');
        } else {
          errorMessage.value = 'Registration successful, but failed to login automatically.';
        }
      } catch (error: any) {
        console.error('Error during registration:', error);
        if (error.response && error.response.data && error.response.data.email) {
          errorMessage.value = 'Email is already in use.';
        } else {
          errorMessage.value = 'An error occurred during registration.';
        }
      }
    };

    return {
      form,
      errorMessage,
      handleRegister,
    };
  },
});
</script>

<style scoped>
.register-card {
  flex: 1;
  padding: 40px;
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.register-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

.register-card h2 {
  margin-bottom: 20px;
  font-size: 28px;
  color: #333;
}

.form-group {
  margin-bottom: 20px;
  text-align: left;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 2px solid #ff9a9e;
  border-radius: 8px;
  transition: border-color 0.3s ease;
}

.form-group input:focus {
  border-color: #ff6a6a;
}

.register-button {
  background-color: #ff6a6a;
  color: #fff;
  border: none;
  padding: 12px 20px;
  font-size: 18px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 100%;
  margin-top: 20px;
}

.register-button:hover {
  background-color: #e65c5c;
}

.error-message {
  color: red;
  margin-bottom: 15px;
}

@media (max-width: 768px) {
  .register-card {
    padding: 20px;
  }

  .register-card h2 {
    font-size: 24px;
  }

  .form-group label {
    font-size: 14px;
  }

  .form-group input {
    padding: 8px;
    font-size: 14px;
  }

  .register-button {
    padding: 10px;
    font-size: 16px;
  }
}
</style>
