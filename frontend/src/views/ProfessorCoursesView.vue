<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Navbar from '../components/Navbar.vue'

const courses = ref([])
const loading = ref(true)
const error = ref(null)

async function fetchCourses() {
  loading.value = true
  error.value = null
  try {
    const res = await axios.get('/api/cursos', { withCredentials: true })
    const data = res.data
    // Acepta diferentes shapes: { cursos: [...] } | { courses: [...] } | [...]
    courses.value = data.cursos || data.courses || data || []
  } catch (e) {
    error.value = e.response?.data?.message || e.message || String(e)
    console.error('Error cargando cursos:', e)
  } finally {
    loading.value = false
  }
}

onMounted(fetchCourses)
</script>

<template>
    <Navbar />
    <div class="container pt-5">
    <div class="d-flex justify-content-between align-items-center mt-4 mb-3">
      <h2 class="mb-0"><i class="bi bi-book-half text-primary me-2"></i> Cursos Asignados</h2>
        <button class="btn btn-outline-secondary btn-sm" @click="fetchCourses" :disabled="loading">
        <i class="bi bi-arrow-clockwise me-1"></i> Recargar
      </button>
    </div>

    <div class="card shadow-sm">
      <div class="card-body">
        <div v-if="loading" class="text-center">Cargando...</div>
        <div v-else>
            <div v-if="error" class="alert alert-danger text-center">Error: {{ error }}</div>
            <div v-if="courses && courses.length" class="row">
                <div v-for="curso in courses" :key="curso.id || curso.nombre" class="col-md-6 col-lg-4 mb-4">
                    <div class="card curso-card text-center shadow-sm">
                        <div class="card-body">
                            <h5 class="card-title mb-2 nombre-curso">{{ curso.nombre }}</h5>
                            <p class="card-text mb-1"><i class="bi bi-people-fill"></i> {{ curso.student_count }} estudiante<span v-if="curso.student_count !== 1">s</span></p>
                            <p class="card-text"><i class="bi bi-bar-chart-fill"></i> Promedio: <strong>{{ curso.average_score }}</strong></p>
                        </div>
                    </div>
                </div>
            </div>

            <div v-else class="alert alert-info text-center">No hay cursos registrados.</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Mantengo clases existentes; añade estilos locales si lo deseas */
.titulo { font-size: 1.75rem; }
.nombre-curso { font-weight: 600; }
</style>
