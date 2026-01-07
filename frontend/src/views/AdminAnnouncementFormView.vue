<script setup>
import { ref } from 'vue'
import Navbar from '../components/Navbar.vue'
import announcementService from '../services/announcementService'

const title = ref('')
const content = ref('')
const isPrivate = ref(false)
const courseId = ref('')
const loading = ref(false)
const message = ref(null)

async function submit() {
  loading.value = true
  message.value = null
  try {
    const payload = {
      title: title.value,
      content: content.value,
      is_private: isPrivate.value,
      course_id: courseId.value || null,
    }
    const res = await announcementService.createAnnouncement(payload)
    if (res?.success) {
      message.value = { type: 'success', text: res.message || 'Anuncio creado correctamente.' }
      title.value = ''
      content.value = ''
      isPrivate.value = false
      courseId.value = ''
    } else {
      message.value = { type: 'error', text: res?.message || 'No se pudo crear el anuncio.' }
    }
  } catch (err) {
    message.value = { type: 'error', text: err.message || 'Error creando el anuncio.' }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <Navbar />
  <div class="container pt-5">
    <div class="d-flex justify-content-between align-items-center mt-4 mb-3">
      <h2 class="mb-0"><i class="bi bi-megaphone text-primary me-2"></i> Nuevo anuncio</h2>
      <router-link to="/anuncios" class="btn btn-outline-secondary btn-sm">Volver</router-link>
    </div>

    <div v-if="message" :class="['alert', message.type === 'error' ? 'alert-danger' : 'alert-success']">{{ message.text }}</div>

    <div class="card shadow-sm">
      <div class="card-body">
        <div class="mb-3">
          <label class="form-label">Título</label>
          <input v-model="title" type="text" class="form-control" placeholder="Ingresa el título" />
        </div>
        <div class="mb-3">
          <label class="form-label">Contenido</label>
          <textarea v-model="content" class="form-control" rows="4" placeholder="Escribe el anuncio"></textarea>
        </div>
        <div class="mb-3 form-check">
          <input v-model="isPrivate" type="checkbox" id="isPrivate" class="form-check-input" />
          <label class="form-check-label" for="isPrivate">Anuncio privado (visible solo para curso asociado)</label>
        </div>
        <div class="mb-3">
          <label class="form-label">ID de curso (opcional)</label>
          <input v-model="courseId" type="number" class="form-control" placeholder="Ej: 10" />
        </div>
        <div class="text-end">
          <button class="btn btn-primary" :disabled="loading" @click="submit">
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            Crear anuncio
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
