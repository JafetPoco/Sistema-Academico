<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Navbar from '../components/Navbar.vue'

const publicAnnouncements = ref([])
const privateAnnouncements = ref([])
const role = ref(null)
const loading = ref(true)

// Ajusta base si tu backend corre en otro host/puerto
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5000'

async function loadAnnouncements() {
  loading.value = true
  try {
    const res = await axios.get(`${API_BASE}/api/anuncios`)
    publicAnnouncements.value = res.data.public_announcements || []
    privateAnnouncements.value = res.data.private_announcements || []
    role.value = res.data.role ?? null
  } catch (err) {
    console.error('Error cargando anuncios:', err)
  } finally {
    loading.value = false
  }
}

onMounted(loadAnnouncements)
</script>

<template>
  <Navbar />

  <div class="container pt-6">
    <div v-if="loading" class="text-center py-4">Cargando...</div>

    <div v-else>
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="mb-0">
          <i class="bi bi-megaphone-fill text-primary me-2"></i>
          Anuncios
        </h2>
        <router-link v-if="role === 2" to="/anuncios/create" class="btn btn-outline-primary">
          <i class="bi bi-plus-circle me-1"></i> Crear nuevo anuncio
        </router-link>
      </div>

      <div class="card mb-5 shadow-sm">
        <div class="card-header bg-primary text-white">
          <i class="bi bi-globe-americas me-2"></i> Anuncios Públicos
        </div>
        <ul class="list-group list-group-flush">
          <li v-for="anuncio in publicAnnouncements" :key="anuncio.id ?? anuncio.title" class="list-group-item">
            <strong>{{ anuncio.title }}</strong><br>
            <small class="text-muted">{{ anuncio.content }}</small>
          </li>
          <li v-if="!publicAnnouncements.length" class="list-group-item text-muted text-center">
            No hay anuncios públicos disponibles.
          </li>
        </ul>
      </div>

      <div v-if="privateAnnouncements.length" class="card shadow-sm">
        <div class="card-header bg-dark text-white">
          <i class="bi bi-shield-lock me-2"></i> Anuncios Privados
        </div>
        <ul class="list-group list-group-flush">
          <li v-for="anuncio in privateAnnouncements" :key="anuncio.id ?? anuncio.title" class="list-group-item">
            <strong>{{ anuncio.title }}</strong><br>
            <small class="text-muted">{{ anuncio.content }}</small>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container { padding-top: 4rem; }
.card-header i { font-size: 1rem; }
</style>
