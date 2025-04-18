<template>
  <div>
    <button @click="toggleChat" class="chat-toggle-button">Chat</button>
    <div v-if="chatOpen" class="chat-container">
      <div class="chat-header">
        <h3>Chat with {{ selectedUser && selectedUser.email ? selectedUser.email : 'Select a user' }}</h3>
        <button @click="toggleChat" class="close-button">×</button>
      </div>
      <div class="user-list" v-if="!selectedUser">
        <div v-for="user in users" :key="user.id" @click="selectUser(user)" class="user-item">
          {{ user.email }}
        </div>
      </div>
      <div class="chat-messages" v-if="selectedUser">
        <div v-for="msg in messages" :key="msg.id" class="message">
          <strong>{{ msg.sender && msg.sender.email ? msg.sender.email : 'Unknown' }}:</strong> {{ msg.message_text }}
        </div>
      </div>
      <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="Type a message..." :disabled="!selectedUser"/>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from '@/plugins/axios';

export default {
  name: 'ChatComponent',
  setup() {
    const chatOpen = ref(false);
    const users = ref([]);
    const messages = ref([]);
    const newMessage = ref('');
    const selectedUser = ref(null);

    const toggleChat = () => {
      chatOpen.value = !chatOpen.value;
      if (!chatOpen.value && selectedUser.value) {
        // Kullanıcı seçiliyken chat kapatıldığında mesajları temizle
        messages.value = [];
        selectedUser.value = null;
      }
    };

    const fetchUsers = async () => {
      try {
        const response = await axios.get('/api/cusers/');
        users.value = response.data;
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    };

    const selectUser = async (user) => {
      selectedUser.value = user;
      await fetchMessages(user.id);
      chatOpen.value = false; // Kullanıcı seçildikten sonra chat'i kapat
    };

    const fetchMessages = async (userId) => {
      if (!userId) return; // Kullanıcı ID'si yoksa işlem yapma
      try {
        const response = await axios.get(`/api/messages/?user=${userId}`);
        messages.value = response.data;
      } catch (error) {
        console.error('Error fetching messages:', error);
      }
    };

    const sendMessage = async () => {
      if (!newMessage.value.trim() || !selectedUser.value) return;

      const message = {
        sender_id: localStorage.getItem('user_id'),
        receiver_id: selectedUser.value.id,
        message_text: newMessage.value,
      };

      try {
        await axios.post('/api/messages/', message);
        messages.value.push({ ...message, sender: { email: 'You' } });
        newMessage.value = '';
      } catch (error) {
        console.error('Error sending message:', error.response.data);
      }
    };

    onMounted(fetchUsers);

    return {
      chatOpen,
      users,
      messages,
      newMessage,
      selectedUser,
      toggleChat,
      selectUser,
      sendMessage,
    };
  }
};
</script>

<style scoped>
.chat-toggle-button {
  position: fixed;
  bottom: 10px;
  right: 10px;
  background-color: #4a90e2;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 50%;
  cursor: pointer;
}

.chat-container {
  position: fixed;
  bottom: 60px;
  right: 10px;
  width: 300px;
  height: 400px;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

.chat-header {
  background-color: #4a90e2;
  color: white;
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 10px 10px 0 0;
}

.user-list {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
}

.user-item {
  padding: 5px;
  cursor: pointer;
  border-bottom: 1px solid #ddd;
}

.user-item:hover {
  background-color: #f0f0f0;
}

.chat-messages {
  flex: 1;
  padding: 10px;
  overflow-y: auto;
}

.message {
  margin-bottom: 10px;
}

input {
  border: none;
  border-top: 1px solid #ccc;
  padding: 10px;
  font-size: 16px;
  border-radius: 0 0 10px 10px;
}
</style>
