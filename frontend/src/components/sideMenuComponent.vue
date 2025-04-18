<template>
  <div>
    <button v-if="loggedIn" @click="toggleMenu" class="menu-toggle-button">
      ☰
    </button>
    <div :class="{ 'side-menu': true, 'open': isMenuOpen }">
      <div class="side-menu-header">
        <h2>FitCamp</h2>
        <button @click="toggleMenu" class="close-button">×</button>
        <img :src="getProfilePicture(userProfile?.profile_pic)" alt="Profile Picture" class="profile-picture" />
        <h3>{{ userProfile?.first_name }} {{ userProfile?.last_name }}</h3>
        <button v-if="isOwnProfile()" @click="editProfile" class="edit-button">Edit Profile</button>
      </div>
      <ul>
        <li v-for="link in menuLinks" :key="link.name" @click="navigateTo(link.path)">
          <div class="menu-item">
            <i :class="link.icon"></i>
            <span>{{ link.name }}</span>
          </div>
        </li>
        <li @click="logout">
          <div class="menu-item">
            <i class="fas fa-sign-out-alt"></i>
            <span>Logout</span>
          </div>
        </li>
      </ul>
    </div>
    <div v-if="isMenuOpen" class="overlay" @click="toggleMenu"></div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import apiClient from '@/plugins/axios';
import defaultAvatar from '@/assets/default-avatar.png';

interface MenuLink {
  name: string;
  path: string;
  icon: string;
}

export default defineComponent({
  name: 'SideMenuComponent',
  setup() {
    const router = useRouter();
    const menuLinks = ref<MenuLink[]>([]);
    const isMenuOpen = ref(false);
    const loggedIn = ref(!!localStorage.getItem('access_token'));
    const userProfile = ref<any>(null);

    const toggleMenu = () => {
      isMenuOpen.value = !isMenuOpen.value;
    };

    const navigateTo = (path: string) => {
      router.push(path);
      toggleMenu();
    };

    const loadMenuLinks = async () => {
      if (!loggedIn.value) return;

      try {
        const userId = localStorage.getItem('user_id');
        const isTrainer = localStorage.getItem('is_trainer') === 'true';
        const response = await apiClient.get(`/api/profile/${userId}`);
        userProfile.value = response.data;

        const commonLinks = [
          { name: 'Home', path: '/', icon: 'fas fa-home' },
          { name: 'Dashboard', path: isTrainer ? '/trainer-dashboard' : '/student-dashboard', icon: isTrainer ? 'fas fa-chalkboard-teacher' : 'fas fa-user-graduate' },
          { name: 'Profile', path: `/profile/${userId}`, icon: 'fas fa-user' },
          { name: 'Messages', path: '/messages', icon: 'fas fa-clipboard-list' },
          { name: 'Blog', path: '/blog', icon: 'fas fa-blog' },
          { name: 'Exercises', path: '/exercises', icon: 'fas fa-dumbbell' },
          { name: 'Calculations', path: '/calculations', icon: 'fas fa-calculator' },
          { name: 'Trainers', path: '/trainers', icon: 'fas fa-users' },
          { name: 'SubPlans', path: '/plans', icon: 'fas fa-clipboard-list' }
        ];

        menuLinks.value = commonLinks;
      } catch (error) {
        console.error('Error fetching profile:', error);
        router.push('/login');
      }
    };

    const getProfilePicture = (path: string | null) => {
      return path ? `${apiClient.defaults.baseURL}${path}` : defaultAvatar;
    };

    const isOwnProfile = () => {
      const userId = localStorage.getItem('user_id');
      return userProfile.value?.user_id === Number(userId);
    };

    const editProfile = () => {
      router.push(`/profile/${localStorage.getItem('user_id')}`);
    };

    const logout = async () => {
      try {
        await apiClient.post('/api/logout/', {
          refresh: localStorage.getItem('refresh_token')
        }, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user_id');
        localStorage.removeItem('is_trainer');
        loggedIn.value = false;
        router.push('/login');
      } catch (error) {
        console.error('Logout failed:', error);
        alert('Logout failed, please try again.');
      }
    };

    onMounted(() => {
      loadMenuLinks();
    });

    return {
      menuLinks,
      isMenuOpen,
      toggleMenu,
      navigateTo,
      userProfile,
      loggedIn,
      getProfilePicture,
      editProfile,
      isOwnProfile,
      logout,
    };
  },
});
</script>

<style scoped>
.side-menu {
  position: fixed;
  left: 0;
  top: 0;
  width: 250px;
  height: 100%;
  background: #ffffff; /* White background color */
  padding: 20px;
  transition: transform 0.3s ease;
  transform: translateX(-100%);
  z-index: 1000;
  display: flex;
  flex-direction: column;
  color: #333333; /* Text color */
}

.side-menu.open {
  transform: translateX(0);
}

.side-menu-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
  position: relative;
}

.side-menu-header h2 {
  color: #333333; /* Header text color */
  margin: 0 0 10px;
  font-size: 24px;
}

.side-menu-header h3 {
  color: #333333; /* Header text color */
  margin: 10px 0 0 0;
  font-size: 18px;
}

.edit-button {
  background-color: #e65c5c;
  color: white;
  border: none;
  padding: 10px 20px;
  margin-top: 10px;
  cursor: pointer;
  border-radius: 5px;
}

.side-menu ul {
  list-style: none;
  padding: 0;
  flex-grow: 1;
}

.side-menu li {
  margin-bottom: 15px;
}

.menu-item {
  display: flex;
  align-items: center;
  background: #f0f0f0; /* Background color for menu items */
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.menu-item:hover {
  background: #e65c5c; /* Hover background color */
}

.menu-item i {
  margin-right: 10px;
}

.menu-item span {
  font-size: 18px;
}

.menu-toggle-button {
  position: fixed;
  top: 20px;
  left: 20px;
  background: #e65c5c; /* Button background color */
  color: white;
  border: none;
  padding: 10px;
  cursor: pointer;
  border-radius: 5px;
  z-index: 1100;
}

.menu-toggle-button:hover {
  background: #333333; /* Button hover background color */
}

.close-button {
  position: absolute;
  top: 20px;
  right: 20px;
  background: none;
  border: none;
  font-size: 20px;
  color: #333333; /* Close button color */
  cursor: pointer;
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5); /* Overlay background */
  z-index: 900;
}

.profile-picture {
  width: 80px;
  height: 80px;
  border-radius: 50%; /* Circular profile pictures */
  object-fit: cover; /* Ensures the image fits without stretching */
  margin-bottom: 10px; /* Space below the profile picture */
}
</style>
