<template>
  <div class="video-detail" v-if="video">
    <div class="video-header">
      <h1>{{ video.title }}</h1>
    </div>
    <div class="video-container">
      <iframe :src="video.video_url" frameborder="0" allowfullscreen class="video-frame"></iframe>
    </div>
    <div v-if="video.instructions && video.instructions.length > 0" class="instructions">
      <h2>Instructions</h2>
      <ol>
        <li v-for="instruction in video.instructions" :key="instruction.step_number">
          <strong>Step {{ instruction.step_number }}:</strong> {{ instruction.instruction_text }}
        </li>
      </ol>
    </div>
  </div>
  <div v-else class="loading">
    <div class="spinner"></div>
    Loading...
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, watch } from 'vue';
import axios from 'axios';
import { useRoute } from 'vue-router';

interface Instruction {
  step_number: number;
  instruction_text: string;
}

interface ExerciseVideo {
  title: string;
  video_url: string;
  instructions: Instruction[];
}

export default defineComponent({
  name: 'ExerciseDetail',
  setup() {
    const route = useRoute();
    const video = ref<ExerciseVideo | null>(null);

    const fetchVideo = async (slug: string) => {
      try {
        console.log('Fetching video for slug:', slug);
        const response = await axios.get(`http://localhost:8000/api/video/${slug}/`);
        console.log(response.data);  // Konsola gelen veriler
        video.value = response.data;
      } catch (error) {
        console.error('Error fetching video details:', error);
      }
    };

    watch(
      () => route.params.slug,
      (newSlug) => {
        if (newSlug) {
          fetchVideo(newSlug as string);
        }
      },
      { immediate: true }
    );

    return {
      video
    };
  }
});
</script>

<style scoped>
.video-detail {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.video-header {
  text-align: center;
  margin-bottom: 20px;
}

h1 {
  font-size: 28px;
  color: #333;
}

.video-container {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.video-frame {
  width: 100%;
  height: 450px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.instructions {
  background: #ffffff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.instructions h2 {
  margin-bottom: 15px;
  color: #444;
  text-align: left;
}

.instructions ol {
  padding-left: 20px;
  list-style: none; 
}

.instructions li {
  margin-bottom: 10px;
  line-height: 1.6;
  font-size: 16px;
  text-align: left;
}

.instructions li strong {
  color: #444;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  text-align: center;
  font-size: 18px;
  color: #555;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-left-color: #333;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .video-frame {
    height: 300px;
  }
}

@media (max-width: 480px) {
  .video-frame {
    height: 200px;
  }
}
</style>
