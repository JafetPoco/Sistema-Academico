import { createRouter, createWebHistory } from 'vue-router'
import MainView from '../views/mainView.vue'
import AdminUsersView from '../views/AdminUsersView.vue'
import ParentGradesView from '../views/ParentGradesView.vue'
import AdminCoursesView from '../views/AdminCoursesView.vue'
import ReportsView from '../views/ReportesView.vue'
import QualificationFormView from '../views/QualificationFormView.vue'
import ProfessorCoursesView from '../views/ProfessorCoursesView.vue'
import AdminAnnouncementFormView from '../views/AdminAnnouncementFormView.vue'

const routes = [
  { path: '/', name: 'Home', component: MainView },
  { path: '/anuncios', name: 'Anuncios', component: () => import('../views/AnunciosView.vue') },
  { path: '/login', name: 'Login', component: () => import('../views/LoginView.vue') },
  { path: '/profile', name: 'Profile', component: () => import('../views/ProfileView.vue') },
  { path: '/dashboard', name: 'Dashboard', component: () => import('../views/DashboardView.vue') },
  { path: '/register', name: 'Register', component: () => import('../views/RegisterView.vue') },
  { path: '/admin/users', name: 'AdminUsers', component: AdminUsersView },
  { path: '/grades/parent', name: 'ParentGrades', component: ParentGradesView },
  { path: '/admin/courses', name: 'AdminCourses', component: AdminCoursesView },
  { path: '/reportes', name: 'Reportes', component: ReportsView },
  { path: '/calificaciones/form', name: 'QualificationForm', component: QualificationFormView },
  { path: '/courses/professor', name: 'ProfessorCoursesView', component: ProfessorCoursesView },
  { path: '/anuncios/create', name: 'CreateAnnouncement', component: AdminAnnouncementFormView },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
