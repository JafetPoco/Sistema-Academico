<script setup>
import { ref, onMounted } from 'vue'
import Navbar from '../components/Navbar.vue'
import announcementService from '../services/announcementService'

const title = ref('')
const content = ref('')
const isPrivate = ref(false)
const courseId = ref('')
const loading = ref(false)
const message = ref(null)
const courses = ref([])

const loadingCourses = ref(false)
const menssageCourses = ref(null)

async function loadCourses() {
  loadingCourses.value = true
  menssageCourses.value = null
  try {
    const res = await announcementService.fetchCourses()
    if (Array.isArray(res)) courses.value = res
    else if (Array.isArray(res.data)) courses.value = res.data
    else if (Array.isArray(res.cursos)) courses.value = res.cursos
    else courses.value = []
  } catch (err) {
    menssageCourses.value = { type: 'error', text: err.message || 'Error cargando cursos.' }
  } finally {
    loadingCourses.value = false
  }
}

onMounted(loadCourses)

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
          <div class="d-flex align-items-center">
            <select v-model="courseId" class="form-select me-2" :disabled="loadingCourses || menssageCourses">
              <option value="">-- Selecciona un curso --</option>
              <option v-for="curso in courses" :key="curso.id" :value="curso.id">
                {{ curso.name }} (ID: {{ curso.id }})
              </option>
            </select>
            <div v-if="loadingCourses" class="spinner-border spinner-border-sm text-secondary" role="status" aria-hidden="true"></div>
          </div>
          <div v-if="menssageCourses" class="text-danger mt-2"><i class="bi bi-exclamation-octagon-fill"></i> {{ menssageCourses.text || menssageCourses }}</div>
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
