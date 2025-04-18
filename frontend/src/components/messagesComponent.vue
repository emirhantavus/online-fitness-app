<template>
  <div class="container">
    <div class="sidebar">
      <h3>Users</h3>
      <input v-model="searchQuery" @input="filterUsers" placeholder="Search users..." class="search-input" />
      <div v-if="searchQuery.length >= 4" v-for="user in filteredUsers" :key="user.id" @click="selectUser(user)" class="user-item">
        {{ user.email }}
      </div>
    </div>
    <div class="main">
      <div v-if="selectedUser">
        <div class="chat-header">
          <h3>Chat with {{ selectedUser.email }}</h3>
        </div>
        <div class="chat-messages">
          <div v-for="msg in messages" :key="msg.id" class="message">
            <strong>{{ msg.sender === userId ? userProfile.email : selectedUser.email }}:</strong> {{ msg.message_text }}
          </div>
        </div>
        <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="Type a message..." />
      </div>
      <div v-else>
        <h3>Please select a user to chat with</h3>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import axios from '@/plugins/axios';

interface User {
  id: number;
  email: string;
}

interface Message {
  id: number;
  sender: number;
  receiver: number;
  message_text: string;
}

export default defineComponent({
  name: 'MessagesComponent',
  setup() {
    const users = ref<User[]>([]);
    const filteredUsers = ref<User[]>([]);
    const messages = ref<Message[]>([]);
    const newMessage = ref('');
    const selectedUser = ref<User | null>(null);
    const userId = parseInt(localStorage.getItem('user_id') || '0');
    const searchQuery = ref('');
    const userProfile = ref({ email: '' });

    const fetchUsers = async () => {
      try {
        const response = await axios.get('/api/cusers/');
        users.value = response.data.results;
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    };

    const fetchMessages = async (userId: number) => {
      try {
        const response = await axios.get(`/api/messages/?user=${userId}`);
        messages.value = response.data.results;
      } catch (error) {
        console.error('Error fetching messages:', error);
      }
    };

    const selectUser = async (user: User) => {
      selectedUser.value = user;
      await fetchMessages(user.id);
    };

    const sendMessage = async () => {
      if (!newMessage.value.trim() || !selectedUser.value) return;

      const message = {
        receiver: selectedUser.value.id,
        message_text: newMessage.value,
      };

      try {
        const response = await axios.post('/api/messages/', message);
        messages.value.push(response.data);
        newMessage.value = '';
      } catch (error: any) {
        console.error('Error sending message:', error.response.data);
      }
    };

    const filterUsers = () => {
      const query = searchQuery.value.toLowerCase();
      if (query.length >= 4) {
        filteredUsers.value = users.value.filter(user => user.email.toLowerCase().includes(query));
      } else {
        filteredUsers.value = [];
      }
    };

    const fetchUserProfile = async () => {
      try {
        const response = await axios.get(`/api/profile/${userId}`);
        userProfile.value = response.data;
      } catch (error) {
        console.error('Error fetching user profile:', error);
      }
    };

    onMounted(() => {
      fetchUsers();
      fetchUserProfile();
    });

    return {
      users,
      filteredUsers,
      messages,
      newMessage,
      selectedUser,
      userId,
      searchQuery,
      selectUser,
      sendMessage,
      filterUsers,
      userProfile,
    };
  },
});
</script>

<style scoped>
.container {
  display: flex;
  height: 100vh;
}
.sidebar {
  width: 25%;
  background-color: #f4f4f4;
  padding: 20px;
}
.search-input {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 10px;
  font-size: 16px;
}
.user-item {
  cursor: pointer;
  padding: 10px;
  margin-bottom: 10px;
  background-color: #e0e0e0;
}
.user-item:hover {
  background-color: #c0c0c0;
}
.main {
  width: 75%;
  padding: 20px;
  display: flex;
  flex-direction: column;
}
.chat-header {
  background-color: #4a90e2;
  color: white;
  padding: 10px;
  border-radius: 10px 10px 0 0;
}
.chat-messages {
  flex: 1;
  padding: 10px;
  overflow-y: auto;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 0 0 10px 10px;
}
.message {
  margin-bottom: 10px;
}
input {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 10px;
  font-size: 16px;
}
</style>
