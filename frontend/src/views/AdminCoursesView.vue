<script setup>
import { onMounted, ref } from 'vue'
import Navbar from '../components/Navbar.vue'
import adminService from '../services/adminService'

const courses = ref([])
const professors = ref([])
const loading = ref(false)
const message = ref(null)

// Form data
const courseName = ref('')
const professorId = ref('')

async function loadCourses() {
  loading.value = true
  message.value = null
  try {
    const res = await adminService.fetchCourses()
    courses.value = res.data || []
  } catch (err) {
    message.value = { type: 'error', text: err.message || 'Error cargando cursos.' }
  } finally {
    loading.value = false
  }
}

async function loadProfessors() {
  try {
    const res = await adminService.fetchProfessors()
    professors.value = res.data || []
  } catch (err) {
    // silent fail
  }
}

async function createCourse() {
  if (!courseName.value || !professorId.value) {
    message.value = { type: 'error', text: 'Nombre del curso y profesor son obligatorios.' }
    return
  }
  loading.value = true
  message.value = null
  try {
    const payload = {
      name: courseName.value,
      professor_id: professorId.value,
    }
    const res = await adminService.createCourse(payload)
    if (res?.success) {
      message.value = { type: 'success', text: res.message || 'Curso creado correctamente.' }
      courseName.value = ''
      professorId.value = ''
      await loadCourses()
    } else {
      message.value = { type: 'error', text: res?.message || 'No se pudo crear el curso.' }
    }
  } catch (err) {
    message.value = { type: 'error', text: err.message || 'Error creando curso.' }
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await loadCourses()
  await loadProfessors()
})
</script>

<template>
  <div>
    <Navbar />
    <div class="container pt-5">
      <div class="d-flex justify-content-between align-items-center mt-4 mb-3">
        <h2 class="mb-0"><i class="bi bi-book-half text-info me-2"></i> Gestión de Cursos</h2>
        <button class="btn btn-outline-secondary btn-sm" @click="loadCourses" :disabled="loading">
          <i class="bi bi-arrow-clockwise me-1"></i> Recargar
        </button>
      </div>

      <div v-if="message" :class="['alert', message.type === 'error' ? 'alert-danger' : 'alert-success']">{{ message.text }}</div>

      <!-- Form to create course -->
      <div class="card shadow-sm mb-4">
        <div class="card-header">
          <h5 class="mb-0">Crear Nuevo Curso</h5>
        </div>
        <div class="card-body">
          <div class="row g-3">
            <div class="col-md-6">
              <label class="form-label">Nombre del Curso</label>
              <input v-model="courseName" type="text" class="form-control" placeholder="Ej: Matemáticas Avanzadas" />
            </div>
            <div class="col-md-6">
              <label class="form-label">Profesor Asignado</label>
              <select v-model="professorId" class="form-select">
                <option value="">Selecciona un profesor</option>
                <option v-for="prof in professors" :key="prof.id" :value="prof.id">{{ prof.full_name }}</option>
              </select>
            </div>
          </div>
          <div class="mt-3 text-end">
            <button class="btn btn-primary" :disabled="loading" @click="createCourse">
              <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
              Crear Curso
            </button>
          </div>
        </div>
      </div>

      <!-- List of courses -->
      <div class="card shadow-sm">
        <div class="card-header">
          <h5 class="mb-0">Cursos Existentes</h5>
        </div>
        <div class="card-body p-0">
          <div v-if="loading" class="text-center py-4">
            <div class="spinner-border text-primary" role="status"><span class="visually-hidden">Cargando...</span></div>
          </div>
          <table v-else class="table table-striped mb-0 align-middle">
            <thead class="table-light">
              <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Profesor ID</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="course in courses" :key="course.id">
                <td>{{ course.id }}</td>
                <td>{{ course.name }}</td>
                <td>{{ course.professor_id }}</td>
              </tr>
              <tr v-if="!courses.length">
                <td colspan="3" class="text-center text-muted py-3">No hay cursos registrados.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>