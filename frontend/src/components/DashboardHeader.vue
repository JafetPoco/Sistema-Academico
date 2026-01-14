<script>
import authService from '../services/authService'

export default {
  name: 'DashboardHeader',
  props: {
    userName: { type: String, default: 'Usuario' },
    userRole: { type: Number, default: 2 },
    roleName: { type: String, default: 'Administrador' }
  },
  computed: {
    avatarUrl () {
      return `https://ui-avatars.com/api/?name=${encodeURIComponent(this.userName)}&background=random`
    },
    roleClass () {
      switch (this.userRole) {
        case 0: return 'indicator-student'
        case 1: return 'indicator-teacher'
        case 2: return 'indicator-admin'
        case 3: return 'indicator-parent'
        default: return ''
      }
    },
    greeting () {
      switch (this.userRole) {
        case 0: return '¡Hola Estudiante!'
        case 1: return '¡Hola Profesor!'
        case 2: return '¡Hola Administrador!'
        case 3: return '¡Hola Padre/Madre!'
        default: return '¡Hola!'
      }
    }
  },
  methods: {
    async handleLogout () {
      try {
        await authService.logout()
      } catch (err) {
        console.warn('Logout API failed, continuing to redirect', err)
      }
      // clear any local user cache and navigate to main
      try { localStorage.removeItem('user') } catch (e) {}
      this.$router.push('/')
    }
  }
}
</script>

<template>
  <div class="modern-dashboard-header">
    <div class="container">
      <div class="header-main">
        <div class="user-section">
          <div class="user-avatar-wrapper">
            <img :src="avatarUrl" :alt="userName" class="user-avatar" />
            <div :class="['role-indicator', roleClass]"></div>
          </div>
          <div class="user-info">
            <h1 class="welcome-title">
              {{ greeting }}
            </h1>
            <p class="user-name">{{ userName }}</p>
            <span class="role-pill">{{ roleName }}</span>
          </div>
        </div>

        <div class="header-controls">
          <router-link class="nav-chip" to="/"><i class="fas fa-arrow-left"></i> Volver al Inicio</router-link>
          <button class="nav-chip header-btn" @click="handleLogout">
            <i class="bi bi-door-open-fill"></i> Cerrar Sesión
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modern-dashboard-header {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-bottom: 1px solid #dee2e6;
  padding: 1.5rem 0;
  margin-bottom: 2rem;
}

.header-main {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-section { display: flex; align-items: center; gap: 1rem; }
.user-avatar-wrapper { position: relative; }
.user-avatar { width: 60px; height: 60px; border-radius: 50%; object-fit: cover; border: 3px solid white; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.role-indicator { position: absolute; bottom: 0; right: 0; width: 18px; height: 18px; border-radius: 50%; border: 2px solid white; }
.indicator-student { background: #28a745; }
.indicator-teacher { background: #007bff; }
.indicator-admin { background: #dc3545; }
.indicator-parent { background: #17a2b8; }
.welcome-title { font-size: 1.5rem; font-weight: 700; margin: 0; color: #2d3748; }
.user-name { font-size: 1.1rem; color: #718096; margin: 0; }
.role-pill { display: inline-block; background: #e2e8f0; color: #4a5568; padding: 4px 12px; border-radius: 12px; font-size: 0.8rem; font-weight: 600; }
.header-controls { display: flex; align-items: center; gap: 1rem; }
.nav-chip { display: inline-flex; align-items: center; gap: 0.5rem; padding: 8px 16px; background: white; color: #4a5568; text-decoration: none; border-radius: 20px; font-size: 0.9rem; font-weight: 500; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.nav-chip:hover { background: #edf2f7; color: #2d3748; }
.header-btn { border: none; background: transparent; cursor: pointer; }

</style>