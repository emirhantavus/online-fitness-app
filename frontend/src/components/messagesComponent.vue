<template>
  <div class="container">
    <div class="sidebar">
      <h3>Conversations</h3>
      <input v-model="searchQuery" @input="filterUsers" placeholder="Search..." class="search-input" />
      <div v-for="user in conversationUsers" :key="user.id" @click="selectUser(user)" class="user-item">
        {{ user.email }}
        <span v-if="lastMessages[user.id]" class="last-message">{{ lastMessages[user.id] }}</span>
      </div>
    </div>
    <div class="main">
      <div v-if="selectedUser">
        <div class="chat-header">
          <h3>Chat with {{ selectedUser.email }}</h3>
        </div>
        <div class="chat-messages" ref="chatBox">
          <div v-if="sortedMessages.length > 0">
      <div v-for="msg in sortedMessages" :key="msg.id" class="message">
        <strong>{{ msg.sender === userId ? userProfile.email : selectedUser.email }}:</strong>
        {{ msg.message_text }}
      </div>
    </div>
<div v-else>
  <p class="no-messages">Henüz mesaj yok veya yüklenemedi.</p>
</div>
        </div>
        <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="Type a message..." />
      </div>
      <div v-else>
        <h3>Select a conversation</h3>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, onBeforeUnmount, nextTick, computed } from 'vue';
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
  timestamp?: string;
}

export default defineComponent({
  name: 'MessagesComponent',
  setup() {
    const users = ref<User[]>([]);
    const conversationUsers = ref<User[]>([]);
    const messages = ref<Message[]>([]);
    const selectedUser = ref<User | null>(null);
    const newMessage = ref('');
    const userId = parseInt(localStorage.getItem('user_id') || '0');
    const searchQuery = ref('');
    const userProfile = ref<User>({ id: 0, email: '' });
    const lastMessages = ref<Record<number, string>>({});
    const chatBox = ref<HTMLElement | null>(null);
    let socket: WebSocket | null = null;

    const sortedMessages = computed(() =>
      [...messages.value].sort((a, b) => new Date(a.timestamp || '').getTime() - new Date(b.timestamp || '').getTime())
    );

    const scrollToBottom = () => {
      nextTick(() => {
        chatBox.value?.scrollTo({ top: chatBox.value.scrollHeight, behavior: 'smooth' });
      });
    };

    const fetchUsers = async () => {
      const res = await axios.get('/api/cusers/');
      users.value = res.data.results;
      conversationUsers.value = [...res.data.results];
    };

    const fetchMessages = async (receiverId: number) => {
  try {
    const res = await axios.get(`/api/messages/?user=${receiverId}`);
    const msgList = res.data?.results || res.data;
    if (!Array.isArray(msgList)) {
      console.error('Mesaj listesi düzgün gelmedi:', res.data);
      messages.value = [];
      return;
    }
    messages.value = msgList;
    const lastMsg = msgList.length > 0 ? msgList[msgList.length - 1].message_text : undefined;
    if (lastMsg) updateLastMessage(receiverId, lastMsg);
    scrollToBottom();
  } catch (error) {
    console.error('Mesajlar çekilirken hata:', error);
    messages.value = [];
  }
};

    const updateLastMessage = (partnerId: number, message: string) => {
      lastMessages.value[partnerId] = message;
      if (!conversationUsers.value.some(u => u.id === partnerId)) {
        const user = users.value.find(u => u.id === partnerId);
        if (user) conversationUsers.value.push(user);
      }
    };

    const selectUser = async (user: User) => {
      selectedUser.value = user;
      await fetchMessages(user.id);
      setupWebSocket();
    };

    const sendMessage = async () => {
      if (!newMessage.value.trim() || !selectedUser.value) return;
      const payload = {
        receiver: selectedUser.value.id,
        message_text: newMessage.value,
      };
      const res = await axios.post('/api/messages/', payload);

      socket?.send(JSON.stringify({
        sender: res.data.sender,
        receiver: res.data.receiver,
        message_text: res.data.message_text,
        timestamp: res.data.timestamp,
        id: res.data.id,
      }));
      newMessage.value = '';
    };

    const setupWebSocket = () => {
      if (!selectedUser.value) return;
      const otherId = selectedUser.value.id;
      const room = userId < otherId ? `${userId}-${otherId}` : `${otherId}-${userId}`;
      const wsUrl = `ws://localhost:8000/ws/chat/${room}/`;

      if (socket) socket.close();
      socket = new WebSocket(wsUrl);

      socket.onmessage = async (event) => {
  const data = JSON.parse(event.data);

  if (data.sender !== userId && selectedUser.value?.id === data.sender || selectedUser.value?.id === data.receiver) {
    messages.value.push(data);
    scrollToBottom();
  }
};

      socket.onclose = () => console.warn('WebSocket closed');
      socket.onerror = (e) => console.error('WebSocket error', e);
    };

    const filterUsers = () => {
      const q = searchQuery.value.toLowerCase();
      conversationUsers.value = q
        ? users.value.filter(u => u.email.toLowerCase().includes(q))
        : [...users.value];
    };

    const fetchUserProfile = async () => {
      const res = await axios.get(`/api/profile/${userId}`);
      userProfile.value = res.data;
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
      conversationUsers,
      sortedMessages,
      selectedUser,
      newMessage,
      userId,
      searchQuery,
      userProfile,
      lastMessages,
      selectUser,
      sendMessage,
      filterUsers,
      chatBox,
    };
  }
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
  margin-left: 8px;
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
  max-height: 60vh;
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
