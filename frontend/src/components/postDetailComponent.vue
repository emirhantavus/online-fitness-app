<template>
  <div class="post-detail-container">
    <div v-if="post" class="post-detail">
      <img v-if="post.image" :src="getImage(post.image)" alt="Post image" class="post-image" />
      <h1>{{ post.title }}</h1>
      <div class="author-info">
        <img v-if="post.author.userprofile && post.author.userprofile.profile_pic" :src="getImage(post.author.userprofile.profile_pic)" alt="Author profile pic" class="author-image">
        <div class="author-details">
          <p>By: {{ post.author.first_name }} {{ post.author.last_name }}</p>
          <p>{{ new Date(post.created_at).toLocaleDateString() }}</p>
        </div>
      </div>
      <div v-html="post.content" class="post-content"></div>
    </div>
    <div v-if="comments.length" class="comments-section">
      <h2>Comments</h2>
      <CommentCard v-for="comment in comments" :key="comment.id" :comment="comment" />
    </div>
    <div v-else class="no-comments">
      <p>No comments yet.</p>
    </div>
    <div v-if="isAuthenticated" class="comment-form">
      <h2>Add a Comment</h2>
      <textarea v-model="newComment" placeholder="Add a comment..."></textarea>
      <button @click="addComment">Post Comment</button>
    </div>
    <div v-else class="login-prompt">
      <p>You need to be logged in to post a comment.</p>
    </div>
    <div v-else class="loading"></div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import axios from 'axios';
import { useRoute } from 'vue-router';
import CommentCard from '@/components/commendCard.vue';

interface UserProfile {
  profile_pic: string | null;
  bio: string;
  location: string;
  birth_date: string | null;
}

interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  userprofile: UserProfile | null;
}

interface Comment {
  id: number;
  post: number;
  author: User;
  content: string;
  created_at: string;
}

interface Post {
  id: number;
  title: string;
  author: User;
  image: string | null;
  slug: string;
  content: string;
  created_at: string;
}

export default defineComponent({
  name: 'PostDetail',
  components: {
    CommentCard
  },
  setup() {
    const post = ref<Post | null>(null);
    const comments = ref<Comment[]>([]);
    const newComment = ref<string>('');
    const isAuthenticated = ref<boolean>(false);
    const route = useRoute();

    onMounted(async () => {
      const slug = route.params.slug as string;
      const response = await axios.get(`http://localhost:8000/api/posts/${slug}/`);
      post.value = response.data;

      // Yorumları yükle
      if (post.value) {
        const commentsResponse = await axios.get(`http://localhost:8000/api/comments/?post=${post.value.id}`);
        comments.value = commentsResponse.data.results;
      }

      // Kullanıcının kimliğini kontrol et
      try {
        const authResponse = await axios.get('http://localhost:8000/api/profile/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        isAuthenticated.value = authResponse.status === 200;
      } catch (error) {
        isAuthenticated.value = false;
      }
    });

    const getImage = (imagePath: string) => {
      return `${imagePath}`;
    };

    const addComment = async () => {
      if (newComment.value.trim() && post.value) {
        const response = await axios.post('http://localhost:8000/api/comments/', {
          post: post.value.id,
          content: newComment.value,
        }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        comments.value.push(response.data);
        newComment.value = '';
      }
    };

    return { post, comments, newComment, getImage, addComment, isAuthenticated };
  }
});
</script>

<style scoped>
.post-detail-container {
  padding: 40px;
  max-width: 800px;
  margin: 50px auto;
}

.post-detail {
  background: #fff;
  padding: 20px;
}

.post-image {
  width: 100%;
  height: auto;
  max-height: 400px;
  object-fit: cover;
}

h1 {
  font-size: 32px;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.author-info {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.author-image {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

.author-details {
  display: flex;
  flex-direction: column;
}

.author-details p {
  margin: 0;
  color: #777;
}

.author-details p:first-of-type {
  font-size: 14px;
}

.author-details p:last-of-type {
  font-size: 12px;
  color: #aaa;
}

.post-content {
  font-size: 16px;
  line-height: 1.6;
  color: #555;
}

.comments-section {
  margin-top: 40px;
}

.comments-section h2 {
  margin-bottom: 20px;
  font-size: 24px;
}

.comment-card {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  overflow-wrap: break-word;
  word-wrap: break-word;
  hyphens: auto;
}

.comment-date {
  font-size: 12px;
  color: #aaa;
  position: absolute;
  bottom: 10px;
  right: 20px;
}

.no-comments {
  margin-top: 40px;
  text-align: center;
}

.comment-form {
  display: flex;
  flex-direction: column;
  margin-top: 40px;
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
}

.comment-form h2 {
  margin-bottom: 10px;
}

.comment-form textarea {
  padding: 10px;
  border: 2px solid #ff6a6a;
  border-radius: 8px;
  font-size: 16px;
  margin-bottom: 10px;
  resize: vertical;
}

.comment-form button {
  background-color: #ff6a6a;
  color: #fff;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.comment-form button:hover {
  background-color: #e65c5c;
}

.login-prompt {
  text-align: center;
  margin-top: 40px;
}

.loading {
  font-size: 18px;
  color: #555;
  text-align: center;
}

@media (max-width: 768px) {
  .post-detail-container {
    padding: 20px;
    margin: 20px auto;
  }

  .post-detail {
    padding: 15px;
  }

  h1 {
    font-size: 28px;
  }

  .author-image {
    width: 30px;
    height: 30px;
    margin-right: 8px;
  }

  .author-details p:first-of-type {
    font-size: 12px;
  }

  .author-details p:last-of-type {
    font-size: 10px;
  }

  .post-content {
    font-size: 14px;
  }

  .comments-section h2 {
    font-size: 20px;
  }

  .comment-card {
    padding: 15px;
  }

  .comment-form {
    padding: 15px;
  }

  .comment-form textarea {
    font-size: 14px;
  }

  .comment-form button {
    font-size: 14px;
    padding: 8px 16px;
  }
}
</style>
