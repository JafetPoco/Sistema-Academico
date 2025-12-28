<script>
export default {
  name: 'AdminContent',
  data () {
    return {
      cards: [
        { id: 'card-usuarios', title: 'Usuarios', text: 'Ve todos los usuarios registrados en el sistema', to: '/admin/users', btnText: 'Ver Usuarios', btnClass: 'btn-success', icon: 'bi bi-people-fill', iconColor: 'text-success' },
        { id: 'card-anuncios', title: 'Anuncios', text: 'Ve los anuncios publicados en el sistema', to: '/anuncios', btnText: 'Ver Anuncios', btnClass: 'btn-primary', icon: 'bi bi-megaphone-fill', iconColor: 'text-primary' },
        { id: 'card-perfil', title: 'Mi Perfil', text: 'Actualiza tu información personal', to: '/user/profile', btnText: 'Ver Perfil', btnClass: 'btn-info', icon: 'bi bi-person-fill', iconColor: 'text-info' },
        { id: 'card-cursos', title: 'Cursos', text: 'Crea un nuevo curso en el sistema', to: '/admin/courses', btnText: 'Crear Curso', btnClass: 'btn-info', icon: 'bi bi-book-half', iconColor: 'text-info' }
      ]
    }
  }
}
</script>

<template>
  <div class="row g-4">
    <div class="col-md-4" v-for="card in cards" :key="card.id">
      <div class="card dashboard-card h-100 shadow-sm" :id="card.id">
        <div class="card-body text-center">
          <div class="mb-3">
            <i :class="card.icon + ' fs-1 ' + card.iconColor"></i>
          </div>
          <h5 class="card-title" :id="`card-title-${card.id}`">{{ card.title }}</h5>
          <p class="card-text">{{ card.text }}</p>
          <router-link :to="card.to" class="btn" :class="card.btnClass">{{ card.btnText }}</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-card { border-radius: 10px; }
.card-title { margin-bottom: 0.5rem; }
.btn { margin-top: 0.8rem; }
</style>
