<template>
  <div>
    <div class="hero-section">
      <div class="slider">
        <div class="slides" :style="{ transform: `translateX(-${currentSlide * 100}%)` }">
          <div class="slide" v-for="(banner, index) in banners" :key="index">
            <img :src="banner.img" :alt="banner.alt_text" class="slide-image" />
          </div>
        </div>
        <button class="prev" @click="prevSlide">&#10094;</button>
        <button class="next" @click="nextSlide">&#10095;</button>
      </div>
    </div>

    <section class="about-section">
      <h2>About FitCamp</h2>
      <p>FitCamp helps you achieve your fitness goals with top-notch facilities and expert trainers. Our mission is to empower individuals to lead healthier lifestyles through personalized fitness programs and community support.</p>
      
      <br>
      
      <p>We have the latest fitness technology and specialized zones for strength training, HIIT workouts, yoga, and pilates. Our expert trainers provide tailored workout plans and ongoing support to help you reach your fitness milestones.</p>
      
      <br>
      
      <p>Join our vibrant community that fosters camaraderie and mutual encouragement. We host regular classes, workshops, and events to keep you motivated. FitCamp is not just a gym – it's a hub of wellness and motivation.</p>
    </section>

    <section class="calculations-section">
      <h2>Fitness Calculations</h2>
      <div class="calculations-grid">
        <div class="calculation-card" v-for="calculation in calculations" :key="calculation.id" @click="navigateTo(calculation.link)">
          <h3>{{ calculation.title }}</h3>
          <p>{{ calculation.description }}</p>
          <button class="cta-button">Calculate</button>
        </div>
      </div>
    </section>

    <section class="blog-section">
      <h2>Latest Articles</h2>
      <div class="blog-grid">
        <div class="blog-card" v-for="article in blogArticles" :key="article.id">
          <img :src="article.image" :alt="article.title" class="blog-image" />
          <h3>{{ article.title }}</h3>
          <p>{{ article.excerpt }}</p>
          <button class="cta-button" @click="navigateToArticle(article.slug)">Read More</button>
        </div>
      </div>
    </section>

    <section class="exercises-section">
      <h2>Latest Exercises</h2>
      <div class="exercises-grid">
        <div class="exercise-card" v-for="exercise in exercises" :key="exercise.id">
          <img :src="exercise.image || defaultExerciseImage" :alt="exercise.title" class="exercise-image" />
          <h3>{{ exercise.title }}</h3>
          <button class="cta-button" @click="navigateToExercise(exercise.slug)">Watch Video</button>
        </div>
      </div>
    </section>

    <section class="contact-section">
      <h2>Contact Us</h2>
      <form class="contact-form" @submit.prevent="sendEmail">
        <input type="text" v-model="contactForm.name" placeholder="Your Name" required />
        <input type="email" v-model="contactForm.email" placeholder="Your Email" required />
        <textarea v-model="contactForm.message" placeholder="Your Message" required></textarea>
        <button type="submit" class="cta-button">Send Message</button>
      </form>
    </section>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import apiClient from '@/plugins/axios';

interface Banner {
  img: string;
  alt_text: string;
}

interface BlogArticle {
  id: number;
  title: string;
  excerpt: string;
  image: string;
  slug: string;
}

interface Calculation {
  id: number;
  title: string;
  description: string;
  link: string;
}

interface Exercise {
  id: number;
  title: string;
  image: string;
  slug: string;
}

interface ContactForm {
  name: string;
  email: string;
  message: string;
}

export default defineComponent({
  name: 'HomePage',
  setup() {
    const banners = ref<Banner[]>([]);
    const currentSlide = ref(0);
    const router = useRouter();

    const blogArticles = ref<BlogArticle[]>([]);
    const calculations = ref<Calculation[]>([
      { id: 1, title: 'One Rep Max Calculator', description: 'Find out your one-rep max for different exercises.', link: '/calculations/one-rep-max' },
      { id: 2, title: 'Calorie Needs', description: 'Find out how many calories you need to maintain your weight.', link: '/calculations/daily-calorie-needs' },
      { id: 3, title: 'Macronutrient Calculator', description: 'Determine your optimal macronutrient intake.', link: '/calculations/food-calorie-calculation' },
    ]);

    const exercises = ref<Exercise[]>([]);
    const defaultExerciseImage = 'src/assets/video_logo.png'; // Varsayılan egzersiz resmi

    const contactForm = ref<ContactForm>({
      name: '',
      email: '',
      message: '',
    });

    const fetchBanners = async () => {
      try {
        const response = await apiClient.get('/api/banners/');
        banners.value = response.data;
      } catch (error) {
        console.error('Error fetching banners:', error);
      }
    };

    const fetchBlogArticles = async () => {
      try {
        const response = await apiClient.get('/api/posts/');
        blogArticles.value = response.data.results.slice(0, 3);
      } catch (error) {
        console.error('Error fetching blog articles:', error);
      }
    };

    const fetchExercises = async () => {
      try {
        const response = await apiClient.get('/api/videos/');
        exercises.value = response.data.results.slice(0, 3).map((exercise: Exercise) => ({
          ...exercise,
          image: exercise.image || defaultExerciseImage, // Varsayılan resim atama
        }));
      } catch (error) {
        console.error('Error fetching exercises:', error);
      }
    };

    const navigateTo = (link: string) => {
      router.push(link);
    };

    const navigateToArticle = (slug: string) => {
      router.push(`/blog/${slug}`);
    };

    const navigateToExercise = (slug: string) => {
      router.push(`/exercises/${slug}`);
    };

    const sendEmail = async () => {
      try {
        await apiClient.post('/api/contact/', contactForm.value, {
          headers: {
            'Authorization': ''
          }
        });
        alert('Message sent successfully!');
        contactForm.value.name = '';
        contactForm.value.email = '';
        contactForm.value.message = '';
      } catch (error) {
        console.error('Error sending message:', error);
        alert('Failed to send message.');
      }
    };

    const nextSlide = () => {
      currentSlide.value = (currentSlide.value + 1) % banners.value.length;
    };

    const prevSlide = () => {
      currentSlide.value = (currentSlide.value - 1 + banners.value.length) % banners.value.length;
    };

    onMounted(() => {
      fetchBanners();
      fetchBlogArticles();
      fetchExercises();
    });

    return {
      banners,
      currentSlide,
      blogArticles,
      calculations,
      exercises,
      defaultExerciseImage,
      contactForm,
      nextSlide,
      prevSlide,
      navigateTo,
      navigateToArticle,
      navigateToExercise,
      sendEmail,
    };
  },
});
</script>

<style scoped>
.hero-section {
  position: relative;
  text-align: center;
  color: white;
}

.slider {
  position: relative;
  overflow: hidden;
  width: 100%;
  height: 70vh;
}

.slides {
  display: flex;
  transition: transform 0.5s ease-in-out;
}

.slide {
  min-width: 100%;
  box-sizing: border-box;
}

.slide-image {
  width: 100%;
  height: 70vh;
  object-fit: cover;
}

.carousel-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  background: rgba(0, 0, 0, 0.5);
  padding: 20px;
  border-radius: 10px;
}

.prev,
.next {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  padding: 10px;
  cursor: pointer;
}

.prev {
  left: 10px;
}

.next {
  right: 10px;
}

.cta-button {
  background-color: #ff6a6a;
  color: #fff;
  border: none;
  padding: 15px 30px;
  font-size: 18px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.cta-button:hover {
  background-color: #e65c5c;
}

.about-section,
.services-section,
.calculations-section,
.blog-section,
.contact-section,
.exercises-section {
  padding: 50px 20px;
  text-align: center;
}

.services-grid,
.calculations-grid,
.blog-grid,
.exercises-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.service-card,
.calculation-card,
.blog-card,
.exercise-card {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  width: 300px;
  text-align: left;
}

.service-image,
.blog-image,
.exercise-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 10px 10px 0 0;
}

.contact-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  max-width: 500px;
  margin: 0 auto;
}

.contact-form input,
.contact-form textarea {
  padding: 10px;
  border: 2px solid #ddd;
  border-radius: 5px;
}

.contact-form button {
  background-color: #ff6a6a;
  color: #fff;
  border: none;
  padding: 15px;
  font-size: 18px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.contact-form button:hover {
  background-color: #e65c5c;
}

@media (max-width: 768px) {
  .slide-image {
    height: 50vh;
  }

  .service-card,
  .calculation-card,
  .blog-card,
  .exercise-card {
    width: 100%;
  }
}
</style>
