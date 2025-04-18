<template>
  <header>
    <div class="container">
      <div class="logo">
        <h1>FitCamp</h1>
      </div>
      <div class="menu-icon" @click="toggleMenu">☰</div>
      <nav :class="{ open: isMenuOpen }">
        <ul>
          <li><router-link to="/">Home</router-link></li>
          <li><router-link to="/plans">Plans</router-link></li>
          <li><router-link to="/exercises">Exercises</router-link></li>
          <li><router-link to="/calculations">Calculations</router-link></li>
          <li><router-link to="/blog">Blog</router-link></li>
          <li v-if="!isLoggedIn" class="dropdown">
            <span>Login</span>
            <ul class="dropdown-content">
              <li><router-link to="/login">User Login</router-link></li>
              <li><router-link to="/trainerlogin">Trainer Login</router-link></li>
            </ul>
          </li>
          <li v-if="!isLoggedIn"><router-link to="/register">Register</router-link></li>
          <li v-if="isLoggedIn"><button @click="logout">Logout</button></li>
        </ul>
      </nav>
    </div>
  </header>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import apiClient from '@/plugins/axios';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'HeaderComponent',
  setup() {
    const router = useRouter();
    const isLoggedIn = computed(() => !!localStorage.getItem('access_token'));
    const isMenuOpen = ref(false);

    const toggleMenu = () => {
      isMenuOpen.value = !isMenuOpen.value;
    };

    const logout = async () => {
      try {
        const accessToken = localStorage.getItem('access_token');
        await apiClient.post('/api/logout/', {
          refresh: localStorage.getItem('refresh_token')
        }, {
          headers: {
            'Authorization': `Bearer ${accessToken}`
          }
        });
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        router.push('/login');
      } catch (error: any) {
        console.error('Logout failed:', error.response ? error.response.data : error.message);
      }
    };

    return {
      isLoggedIn,
      logout,
      isMenuOpen,
      toggleMenu,
    };
  },
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

header {
  background-color: #333;
  color: #fff;
  padding: 20px 0;
}

.container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
}

.logo h1 {
  font-family: 'Montserrat', sans-serif;
  font-size: 24px;
  color: #fff;
  margin: 0;
  margin-left: 30px;
}

.menu-icon {
  display: none;
  font-size: 24px;
  cursor: pointer;
}

nav ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
  display: flex;
  align-items: center;
}

nav ul li {
  position: relative;
  margin-left: 20px;
}

nav ul li:first-child {
  margin-left: 0;
}

nav ul li a, nav ul li span {
  color: #fff;
  text-decoration: none;
  font-size: 16px;
  font-weight: bold;
  font-family: 'Montserrat', sans-serif;
}

nav ul li a:hover, nav ul li span:hover {
  color: #ffcc00;
}

nav ul li button {
  background: none;
  border: none;
  color: #fff;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  font-family: 'Montserrat', sans-serif;
}

nav ul li button:hover {
  color: #ffcc00;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: #333;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}

.dropdown-content li {
  color: white;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
  text-align: left;
}

.dropdown-content li a {
  color: white;
  text-decoration: none;
}

.dropdown-content li a:hover {
  background-color: #575757;
}

.dropdown:hover .dropdown-content {
  display: block;
}

@media (max-width: 768px) {
  .menu-icon {
    display: block;
  }

  nav {
    display: none;
    width: 100%;
  }

  nav.open {
    display: block;
  }

  nav ul {
    flex-direction: column;
    align-items: flex-start;
  }

  nav ul li {
    margin: 10px 0;
  }

  nav ul li a, nav ul li span, nav ul li button {
    font-size: 18px;
  }
}
</style>
