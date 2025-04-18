<template>
  <div class="comment-card">
    <div class="comment-author">
      <img v-if="comment.author.userprofile && comment.author.userprofile.profile_pic" :src="getImage(comment.author.userprofile.profile_pic)" alt="Author profile pic" class="author-image">
      <div class="author-details">
        <p>{{ comment.author.first_name }} {{ comment.author.last_name }}</p>
      </div>
    </div>
    <p class="comment-content">{{ comment.content }}</p>
    <p class="comment-date">{{ formattedDate }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import type { PropType } from 'vue';

interface UserProfile {
  profile_pic: string | null;
}

interface User {
  first_name: string;
  last_name: string;
  userprofile: UserProfile | null;
}

interface Comment {
  author: User;
  content: string;
  created_at: string;
}

export default defineComponent({
  name: 'CommentCard',
  props: {
    comment: {
      type: Object as PropType<Comment>,
      required: true
    }
  },
  computed: {
    formattedDate(): string {
      return new Date(this.comment.created_at).toLocaleDateString();
    }
  },
  methods: {
    getImage(imagePath: string) {
      return `${imagePath}`;
    }
  }
});
</script>

<style scoped>
.comment-card {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow-wrap: break-word;
  word-wrap: break-word;
  hyphens: auto;
}

.comment-author {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.author-image {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

.author-details p {
  margin: 0;
  color: #777;
  font-size: 14px;
}

.comment-content {
  white-space: pre-wrap;
}

.comment-date {
  font-size: 12px;
  color: #aaa;
  position: absolute;
  bottom: 10px;
  right: 20px;
}
</style>
