<template>
  <div class="container">
    <div class="sidebar">
      <h3>Users</h3>
      <input v-model="searchQuery" @input="filterUsers" placeholder="Search users..." class="search-input" />
      <div
        v-if="searchQuery.length >= 1"
        v-for="user in filteredUsers"
        :key="user.id"
        @click="selectUser(user)"
        class="user-item"
      >
        {{ user.email }}
        <span v-if="lastMessages[user.id]" class="last-message">{{ lastMessages[user.id] }}</span>
      </div>
    </div>
    <div class="main">
      <div v-if="selectedUser">
        <div class="chat-header">
          <h3>Chat with {{ selectedUser.email }}</h3>
        </div>
        <div class="chat-messages">
          <div v-for="msg in messages" :key="msg.id" class="message">
            <strong>{{ msg.sender === userId ? userProfile.email : selectedUser.email }}:</strong>
            {{ msg.message_text }}
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
import { defineComponent, ref, onMounted, onBeforeUnmount } from 'vue';
import axios from '@/plugins/axios';

export default defineComponent({
  name: 'MessagesComponent',
  setup() {
    const users = ref([]);
    const filteredUsers = ref([]);
    const messages = ref([]);
    const newMessage = ref('');
    const selectedUser = ref(null);
    const userId = parseInt(localStorage.getItem('user_id') || '0');
    const searchQuery = ref('');
    const userProfile = ref({ email: '' });
    const lastMessages = ref<Record<number, string>>({});
    let socket: WebSocket | null = null;

    const fetchUsers = async () => {
      const response = await axios.get('/api/cusers/');
      users.value = response.data.results;
      filteredUsers.value = users.value;
    };

    const fetchMessages = async (receiverId: number) => {
      const response = await axios.get(`/api/messages/?user=${receiverId}`);
      messages.value = response.data.results;
      updateLastMessage(receiverId, response.data.results.at(-1)?.message_text);
    };

    const updateLastMessage = (userId: number, message: string) => {
      if (message) lastMessages.value[userId] = message;
    };

    const selectUser = async (user: any) => {
      selectedUser.value = user;
      await fetchMessages(user.id);
      setupWebSocket();
    };

    const sendMessage = async () => {
      if (!newMessage.value.trim() || !selectedUser.value) return;
      const message = {
        receiver: selectedUser.value.id,
        message_text: newMessage.value,
      };
      const response = await axios.post('/api/messages/', message);
      messages.value.push(response.data);
      updateLastMessage(selectedUser.value.id, response.data.message_text);
      newMessage.value = '';
      socket?.send(JSON.stringify(response.data));
    };

    const filterUsers = () => {
      const query = searchQuery.value.toLowerCase();
      filteredUsers.value = query.length >= 1
        ? users.value.filter((u) => u.email.toLowerCase().includes(query))
        : users.value;
    };

    const fetchUserProfile = async () => {
      const response = await axios.get(`/api/profile/${userId}`);
      userProfile.value = response.data;
    };

    const setupWebSocket = () => {
      if (!selectedUser.value) return;
      const roomName = userId < selectedUser.value.id
        ? `${userId}-${selectedUser.value.id}`
        : `${selectedUser.value.id}-${userId}`;
      const wsUrl = `ws://localhost:8000/ws/chat/${roomName}/`;

      if (socket) socket.close();

      socket = new WebSocket(wsUrl);

      socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.sender && data.receiver) {
          messages.value.push(data);
          updateLastMessage(data.sender === userId ? data.receiver : data.sender, data.message_text);
        }
      };
    };

    onMounted(() => {
      fetchUsers();
      fetchUserProfile();
    });

    onBeforeUnmount(() => {
      socket?.close();
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
      lastMessages,
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
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.user-item:hover {
  background-color: #c0c0c0;
}
.last-message {
  font-size: 12px;
  color: #666;
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
