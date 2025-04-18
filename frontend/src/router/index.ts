import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ExercisesView from '@/views/ExercisesView.vue'
import ExerciseDetail from '../views/ExerciseDetail.vue'
import PlanView from '@/views/PlanView.vue'
import RegisterView from '@/views/RegisterView.vue'
import UserLoginView from '@/views/UserLoginView.vue'
import TrainerLoginView from '@/views/TrainerLoginView.vue'
import FoodCaloriesView from '@/views/FoodCaloriesView.vue'
import CalBodyFatView from '@/views/CalBodyFatView.vue'
import DailyCalView from '@/views/DailyCalView.vue'
import OnermView from '@/views/OnermView.vue'
import UserProfileView from '../views/UserProfileView.vue'
import TrainerDashboardView from '@/views/TrainerDashboardView.vue'
import StudentDashboardView from '@/views/StudentDashboardView.vue'
import BlogListView from '@/views/BlogListView.vue'
import BlogDetailView from '@/views/BlogDetailView.vue'
import TrainerPageView from '@/views/TrainerPageView.vue'
import CalculationsView from '@/views/CalculationsView.vue'
import TrainerDetail from '@/views/TrainerProgramDetailView.vue'
import StudentDetail from '@/views/StudentProgramDetailView.vue'
import PaymentView from '@/views/PaymentView.vue'
import TrainerPaymentView from '@/views/TrainerPaymentView.vue'
import NotFound from '@/views/NotFoundView.vue'
import MessageView from '@/views/MessageView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue')
    },
    {
      path:'/exercises',
      name:'exercises',
      component: ExercisesView
    },
    {
      path:'/exercises/:slug',
      name:'ExerciseDetail',
      component: ExerciseDetail,
      props:true
    },
    {
      path: '/plans',
      name: 'plans',
      component: PlanView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/login',
      name: 'userlogin',
      component: UserLoginView
    },
    {
      path: '/trainerlogin',
      name: 'trainerlogin',
      component: TrainerLoginView
    },
    {
      path: '/calculations',
      name: 'calculations',
      component:CalculationsView
    },
    {
      path: '/calculations/food-calorie-calculation',
      name: 'calorieCalculation',
      component:FoodCaloriesView
    },
    {
      path: '/calculations/body-fat-calculation',
      name: 'bodyfatcalculation',
      component:CalBodyFatView
    },
    {
      path: '/calculations/daily-calorie-needs',
      name: 'dailycal',
      component:DailyCalView,
    },
    {
      path: '/calculations/one-rep-max',
      name: 'onerm',
      component:OnermView,
    },
    {
      path:'/profile/:userId',
      name:'userprofile',
      component: UserProfileView,
      props:true,
    },
    {
      path:'/trainer-profile/:userId',
      name:'trainerprofile',
      component: UserProfileView,
      props:true,
    },
    {
      path:'/trainer-dashboard',
      name:'trainerdashboard',
      component:TrainerDashboardView
    },
    {
      path:'/student-dashboard',
      name:'studentdashboard',
      component:StudentDashboardView
    },
    {
      path:'/blog',
      name:'blog',
      component:BlogListView
    },
    {
      path:'/blog/:slug',
      name:'blogdetail',
      component:BlogDetailView
    },
    {
      path: '/trainers',
      name: 'trainerlist',
      component: TrainerPageView
    },
    {
      path: '/student/programs/:id',
      name: 'studentprogramdetail',
      component: StudentDetail,
      props: true
    },
    {
      path: '/trainer/programs/:id',
      name: 'trainerprogramdetail',
      component: TrainerDetail,
      props: true
    },
    {
      path: '/payment',
      name: 'payment',
      component: PaymentView,
    },
    {
      path: '/trainer-payment',
      name: 'trainer-payment',
      component: TrainerPaymentView,
    },
    {
      path: '/messages',
      name: 'messages',
      component: MessageView
    },
    {
      path: '/admin',
      name: 'admin-redirect',
      redirect: () => {
        window.location.href = 'http://localhost:8000/admin';
        return '/';
      }
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: NotFound
    },
  ]
})


router.beforeEach((to, from, next) => {
  const publicPages = ['/', '/about', '/plans', '/exercises', '/calculations', '/blog', '/register', '/login', '/trainerlogin'];
  const authRequiredPages = [
    /^\/profile\/\d+/,
    /^\/trainer-profile\/\d+/,
    /^\/trainer-dashboard/,
    /^\/student-dashboard/,
    /^\/trainers/,
    /^\/student\/programs\/\d+/,
    /^\/trainer\/programs\/\d+/,
    /^\/payment/,
    /^\/trainer-payment/,
    /^\/messages/
  ];

  const authRequired = authRequiredPages.some(regex => regex.test(to.path));
  const loggedIn = localStorage.getItem('access_token');

  if (authRequired && !loggedIn) {
    return next('/login');
  }

  if (loggedIn && ['/', '/login', '/register', '/trainerlogin'].includes(to.path)) {
    return next();
  }

  next();
});

export default router;