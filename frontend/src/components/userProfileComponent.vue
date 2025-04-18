<template>
  <div class="profile-container">
    <h2>User Profile</h2>
    <div v-if="formProfile" class="profile-content">
      <div class="profile-left">
        <div class="avatar">
          <img :src="getImage(formProfile.userprofile?.profile_pic)" alt="Profile Picture" />
        </div>
        <div class="user-info">
          <p><strong>First Name:</strong> {{ formProfile.first_name }}</p>
          <p><strong>Last Name:</strong> {{ formProfile.last_name }}</p>
          <p><strong>Email:</strong> {{ formProfile.email }}</p>
          <p v-if="formProfile.monthly_rate"><strong>Monthly Salary:</strong> ${{ formProfile.monthly_rate }}</p>
        </div>
      </div>
      <div class="profile-middle">
        <p><strong>Bio:</strong></p>
        <div v-html="formProfile.userprofile?.bio"></div>
      </div>
      <div class="profile-right">
        <button v-if="isCurrentUserProfile" @click="toggleEditForm" class="edit-button">Edit Profile</button>
        <div v-if="showEditForm" class="edit-form">
          <form @submit.prevent="updateProfile">
            <div class="form-group">
              <label for="first_name">First Name:</label>
              <input type="text" id="first_name" v-model="formProfile.first_name" />
            </div>
            <div class="form-group">
              <label for="last_name">Last Name:</label>
              <input type="text" id="last_name" v-model="formProfile.last_name" />
            </div>
            <div v-if="formProfile.monthly_rate" class="form-group">
              <label for="monthly_rate">Monthly Salary:</label>
              <input type="number" id="monthly_rate" v-model="formProfile.monthly_rate" />
            </div>
            <div class="form-group">
              <label for="bio">Bio:</label>
              <ckeditor :editor="editor" v-model="formProfile.userprofile.bio"></ckeditor>
            </div>
            <div class="form-group">
              <label for="profile_pic">Profile Picture:</label>
              <input type="file" id="profile_pic" @change="onFileChange" />
            </div>
            <button type="submit" class="update-button">Update Profile</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import apiClient from '@/plugins/axios';
import defaultAvatar from '@/assets/default-avatar.png';
import CKEditor from '@ckeditor/ckeditor5-vue';
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';

interface UserProfile {
  bio?: string;
  profile_pic?: string;
}

interface Profile {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  monthly_rate?: string;
  userprofile: UserProfile;
}

export default defineComponent({
  name: 'UserProfileView',
  components: {
    ckeditor: CKEditor.component
  },
  setup() {
    const profile = ref<Profile | null>(null);
    const formProfile = ref<Profile>({
      id: 0,
      first_name: '',
      last_name: '',
      email: '',
      userprofile: {
        bio: '',
        profile_pic: '',
      },
    });
    const showEditForm = ref(false);
    const isCurrentUserProfile = ref(false);
    const selectedFile = ref<File | null>(null);
    const route = useRoute();
    const editor = ClassicEditor;

    onMounted(async () => {
      await fetchProfile();
    });

    const fetchProfile = async () => {
      const userId = route.params.userId as string;
      const isTrainer = localStorage.getItem('is_trainer') === 'true';
      const endpoint = isTrainer ? `/api/trainers/${userId}/` : `/api/profile/${userId}/`;
      try {
        const response = await apiClient.get(endpoint);
        console.log('Profile data:', response.data);
        profile.value = response.data as Profile;
        formProfile.value = { ...response.data };
        const currentUserId = localStorage.getItem('user_id');
        isCurrentUserProfile.value = userId === currentUserId;
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    };

    const onFileChange = (event: Event) => {
      const input = event.target as HTMLInputElement;
      if (input.files) {
        selectedFile.value = input.files[0];
      }
    };

    const updateProfile = async () => {
      if (!formProfile.value || !formProfile.value.id) {
        throw new Error('User ID not found in profile');
      }

      const endpoint = isCurrentUserProfile.value && localStorage.getItem('is_trainer') === 'true' ? `/api/trainers/${formProfile.value.id}/` : `/api/profile/${formProfile.value.id}/`;
  const formData = new FormData();
  formData.append('first_name', formProfile.value.first_name);
  formData.append('last_name', formProfile.value.last_name);

  // monthly_rate ve bio için undefined kontrolü
  if (formProfile.value.monthly_rate !== undefined) {
    formData.append('monthly_rate', formProfile.value.monthly_rate);
  }
  if (formProfile.value.userprofile.bio !== undefined) {
    formData.append('userprofile.bio', formProfile.value.userprofile.bio);
  }
  
  // Dosya için undefined kontrolü
  if (selectedFile.value instanceof Blob) {
    formData.append('userprofile.profile_pic', selectedFile.value);
  }

  try {
    await apiClient.patch(endpoint, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    await fetchProfile();
    alert('Profile updated successfully!');
    showEditForm.value = false;
  } catch (error) {
    console.error('Error updating profile:', error);
    alert('Failed to update profile.');
  }
};

    const toggleEditForm = () => {
      showEditForm.value = !showEditForm.value;
    };

    const getImage = (imagePath?: string) => {
      return imagePath ? `${imagePath}` : defaultAvatar;
    };

    return {
      profile,
      formProfile,
      showEditForm,
      updateProfile,
      onFileChange,
      toggleEditForm,
      isCurrentUserProfile,
      defaultAvatar,
      getImage,
      editor,
    };
  }
});
</script>

<style scoped>
/* Same styles as before */
</style>



<style scoped>
.profile-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  background: rgba(217, 175, 175, 0.448);
  border-radius: 16px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  padding: 50px;
}

.profile-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-left,
.profile-middle,
.profile-right {
  width: 100%;
  text-align: center;
  padding: 20px;
}

.avatar img {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
}

.user-info {
  margin-top: 20px;
}

.edit-button,
.update-button {
  padding: 10px 20px;
  margin-top: 10px;
  background-color: #0056b3;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
}

.edit-button:hover,
.update-button:hover {
  background-color: #004494;
}

.edit-form {
  margin-top: 20px;
  padding: 20px;
  background: #f0f0f0;
  border-radius: 8px;
  width: 100%;
}

.form-group {
  margin-bottom: 15px;
  text-align: left;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px;
  margin-top: 10px;
  border: 2px solid #ccc;
  border-radius: 8px;
}

@media (max-width: 768px) {
  .profile-container {
    padding: 30px;
  }

  .profile-left,
  .profile-middle,
  .profile-right {
    padding: 15px;
  }

  .edit-button,
  .update-button {
    font-size: 14px;
    padding: 8px 16px;
  }
}

@media (max-width: 480px) {
  .profile-container {
    padding: 20px;
  }

  .profile-left,
  .profile-middle,
  .profile-right {
    padding: 10px;
  }

  .avatar img {
    width: 100px;
    height: 100px;
  }

  .edit-button,
  .update-button {
    font-size: 12px;
    padding: 6px 12px;
  }
}
</style>