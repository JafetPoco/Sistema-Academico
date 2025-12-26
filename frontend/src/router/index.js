import { createRouter, createWebHistory } from 'vue-router'
import MainView from '../views/mainView.vue'

const routes = [
  { path: '/', name: 'Home', component: MainView },
  { path: '/anuncios', name: 'Anuncios', component: () => import('../views/AnunciosView.vue') },
  { path: '/login', name: 'Login', component: () => import('../views/LoginView.vue') },
  { path: '/profile', name: 'Profile', component: () => import('../views/ProfileView.vue') },
  { path: '/dashboard', name: 'Dashboard', component: () => import('../views/DashboardView.vue') },
  { path: '/register', name: 'Register', component: () => import('../views/RegisterView.vue') }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
