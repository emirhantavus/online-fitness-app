<template>
  <div class="blog-container">
    <h1>Blog Posts</h1>
    <div class="search-bar">
      <input type="text" v-model="searchQuery" @input="handleSearchInput" placeholder="Search by title or author" />
    </div>
    <div class="card-grid">
      <div v-for="post in posts" :key="post.id" class="card" @click="goToPost(post.slug)">
        <img :src="post.image ? getImage(post.image) : getImage('/images/posts/default.jpg')" alt="Post image" class="card-image" />
        <div class="card-content">
          <h2>{{ post.title }}</h2>
          <div class="author-info">
            <img v-if="post.author.userprofile && post.author.userprofile.profile_pic" :src="getImage(post.author.userprofile.profile_pic)" alt="Author profile pic" class="author-image">
            <div class="author-details">
              <p>{{ post.author.first_name }} {{ post.author.last_name }}</p>
              <p>{{ new Date(post.created_at).toLocaleDateString() }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="pagination">
      <button @click="fetchPosts(currentPage - 1)" :disabled="currentPage === 1">Previous</button>
      <span>Page {{ currentPage }}</span>
      <button @click="fetchPosts(currentPage + 1)" :disabled="!nextPage">Next</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, watch } from 'vue';
import axios from 'axios';

interface UserProfile {
  profile_pic: string | null;
  bio: string;
  location: string;
  birth_date: string | null;
}

interface User {
  email: string;
  first_name: string;
  last_name: string;
  userprofile: UserProfile | null;
}

interface Post {
  id: number;
  title: string;
  author: User;
  image: string | null;
  slug: string;
  created_at: string;
}

export default defineComponent({
  name: 'BlogList',
  setup() {
    const posts = ref<Post[]>([]);
    const searchQuery = ref<string>('');
    const currentPage = ref<number>(1);
    const nextPage = ref<boolean>(false);

    const fetchPosts = async (page: number = 1) => {
      if (page < 1) return;
      const response = await axios.get('http://localhost:8000/api/posts/', {
        params: {
          search: searchQuery.value,
          page: page,
        }
      });
      posts.value = response.data.results;
      currentPage.value = page;
      nextPage.value = !!response.data.next;
    };

    onMounted(() => {
      fetchPosts();
    });

    const handleSearchInput = () => {
      fetchPosts(1);  // Arama yapıldığında ilk sayfayı getir
    };

    const goToPost = (postSlug: string) => {
      window.location.href = `/blog/${postSlug}`;
    };

    const getImage = (imagePath: string) => {
      return `${imagePath}`;
    };

    return { posts, searchQuery, currentPage, nextPage, fetchPosts, handleSearchInput, goToPost, getImage };
  }
});
</script>

<style scoped>
.blog-container {
  padding: 40px;
  max-width: 1200px;
  margin: 50px auto;
}

h1 {
  font-size: 32px;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.search-bar {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.search-bar input {
  padding: 10px;
  width: 100%;
  max-width: 400px;
  border: 2px solid #ff6a6a;
  border-radius: 8px;
  font-size: 16px;
}

.card-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  overflow: hidden;
  flex: 1 1 calc(33.333% - 20px);
  max-width: calc(33.333% - 20px);
  display: flex;
  flex-direction: column;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.card-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.card-content {
  padding: 20px;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  justify-content: space-between;
}

.card h2 {
  margin: 0 0 10px;
  font-size: 24px;
  color: #ff6a6a;
}

.author-info {
  display: flex;
  align-items: center;
  margin-top: 10px;
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

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.pagination button {
  background-color: #ff6a6a;
  color: #fff;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  border-radius: 8px;
  cursor: pointer;
  margin: 0 10px;
  transition: background-color 0.3s ease;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.pagination button:hover:not(:disabled) {
  background-color: #e65c5c;
}

/* Responsive styles */
@media (max-width: 768px) {
  .card {
    flex: 1 1 calc(50% - 20px);
    max-width: calc(50% - 20px);
  }

  .card-image {
    height: 120px;
  }
}

@media (max-width: 480px) {
  .card {
    flex: 1 1 100%;
    max-width: 100%;
  }

  .card-image {
    height: 100px;
  }

  .search-bar input {
    width: 100%;
    max-width: 100%;
  }
}
</style>
