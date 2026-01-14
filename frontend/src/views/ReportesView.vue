<script setup>
import { onMounted, ref } from 'vue'
import Navbar from '../components/Navbar.vue'
import reportService from '../services/reportService'

const courses = ref([])
const selectedCourse = ref('')
const report = ref([])
const courseName = ref('')
const loading = ref(false)
const message = ref(null)

async function loadCourses() {
  loading.value = true
  message.value = null
  try {
    const res = await reportService.fetchCourses()
    if (res?.success) {
      courses.value = res.courses || []
    } else {
      message.value = { type: 'error', text: res?.message || 'No se pudieron cargar los cursos.' }
    }
  } catch (err) {
    message.value = { type: 'error', text: err.message || 'Error cargando cursos.' }
  } finally {
    loading.value = false
  }
}

async function loadReport() {
  if (!selectedCourse.value) return
  loading.value = true
  message.value = null
  report.value = []
  courseName.value = ''
  try {
    const res = await reportService.fetchCourseReport(selectedCourse.value)
    if (res?.success) {
      report.value = res.grades || []
      courseName.value = res.course_name || ''
    } else {
      message.value = { type: 'error', text: res?.message || 'No se pudo cargar el reporte.' }
    }
  } catch (err) {
    message.value = { type: 'error', text: err.message || 'Error cargando reporte.' }
  } finally {
    loading.value = false
  }
}

onMounted(loadCourses)
</script>

<template>
  <Navbar />
  <div class="container pt-5">
    <div class="d-flex justify-content-between align-items-center mt-4 mb-3">
      <h2 class="mb-0"><i class="bi bi-bar-chart text-info me-2"></i> Reportes por curso</h2>
      <button class="btn btn-outline-secondary btn-sm" @click="loadCourses" :disabled="loading">
        <i class="bi bi-arrow-clockwise me-1"></i> Recargar
      </button>
    </div>

    <div v-if="message" :class="['alert', message.type === 'error' ? 'alert-danger' : 'alert-success']">{{ message.text }}</div>

    <div class="card shadow-sm mb-4">
      <div class="card-body">
        <label class="form-label">Selecciona un curso</label>
        <div class="d-flex gap-3 align-items-center">
          <select v-model="selectedCourse" class="form-select" :disabled="loading || !courses.length">
            <option value="">Elige un curso</option>
            <option v-for="course in courses" :key="course.id" :value="course.id">{{ course.name }}</option>
          </select>
          <button class="btn btn-primary" :disabled="loading || !selectedCourse" @click="loadReport">
            <span v-if="loading" class="spinner-border spinner-border-sm me-1"></span>
            Ver reporte
          </button>
        </div>
        <small v-if="!courses.length" class="text-muted">No tienes cursos asignados.</small>
      </div>
    </div>

    <div v-if="loading" class="text-center py-4">
      <div class="spinner-border text-primary" role="status"><span class="visually-hidden">Cargando...</span></div>
    </div>

    <div v-else-if="report.length">
      <div class="card shadow-sm">
        <div class="card-header">
          <strong>Curso:</strong> {{ courseName || 'Sin nombre' }}
        </div>
        <div class="card-body p-0">
          <table class="table table-striped mb-0 align-middle">
            <thead class="table-light">
              <tr>
                <th>Estudiante</th>
                <th class="text-end">Nota</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in report" :key="row.student_id">
                <td>{{ row.student_name }}</td>
                <td class="text-end fw-semibold">{{ row.score }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div v-else-if="selectedCourse && !loading" class="alert alert-info">No hay calificaciones para este curso.</div>
  </div>
</template>
