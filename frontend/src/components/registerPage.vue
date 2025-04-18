<template>
  <div class="register-wrapper">
    <div class="register-container">
      <RegisterForm />
      <div class="motivation">
        <h2>Join us and start your journey to a healthier, fitter you!</h2>
        <p>Register now and embrace the change!</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import RegisterForm from './registerComponent.vue';

export default defineComponent({
  name: 'RegisterPage',
  components: {
    RegisterForm,
  },
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

body {
  font-family: 'Poppins', sans-serif;
  background-size: cover;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  margin: 0;
}

.register-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  width: 100%;
  padding: 20px;
  backdrop-filter: blur(10px);
}

.register-container {
  display: flex;
  max-width: 800px;
  width: 100%;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.motivation {
  flex: 1;
  background: linear-gradient(135deg, #ff9a9e, #fad0c4);
  color: #fff;
  padding: 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.motivation h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.motivation p {
  margin: 10px 0 0;
  font-size: 16px;
  text-align: center;
}

@media (max-width: 768px) {
  .register-container {
    flex-direction: column;
  }

  .motivation {
    padding: 20px;
  }

  .motivation h2 {
    font-size: 20px;
  }

  .motivation p {
    font-size: 14px;
  }
}
</style>
