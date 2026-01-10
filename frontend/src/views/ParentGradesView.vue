<script setup>
import { onMounted, ref } from 'vue'
import Navbar from '../components/Navbar.vue'
import gradeService from '../services/gradeService'

const loading = ref(true)
const error = ref('')
const students = ref([])

async function loadGrades() {
  loading.value = true
  error.value = ''
  try {
    const res = await gradeService.fetchParentGrades()
    if (res?.success) {
      students.value = res.data || []
    } else {
      error.value = res?.message || 'No se pudieron cargar las calificaciones.'
    }
  } catch (err) {
    error.value = err.message || 'Error cargando calificaciones.'
  } finally {
    loading.value = false
  }
}

onMounted(loadGrades)
</script>

<template>
  <Navbar />
  <div class="container pt-5">
    <div class="d-flex align-items-center justify-content-between mt-4 mb-3">
      <h2 class="mb-0"><i class="bi bi-card-checklist text-success me-2"></i> Calificaciones de mis hijos</h2>
      <button class="btn btn-outline-secondary btn-sm" @click="loadGrades" :disabled="loading">
        <i class="bi bi-arrow-clockwise me-1"></i> Actualizar
      </button>
    </div>

    <div v-if="loading" class="text-center py-4">
      <div class="spinner-border text-primary" role="status"><span class="visually-hidden">Cargando...</span></div>
      <p class="mt-2">Cargando calificaciones...</p>
    </div>

    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else>
      <div v-if="students.length === 0" class="alert alert-info">No se encontraron hijos o calificaciones.</div>

      <div v-for="student in students" :key="student.id" class="card mb-4 shadow-sm">
        <div class="card-header d-flex justify-content-between align-items-center">
          <div>
            <strong>{{ student.name }}</strong>
            <small class="text-muted d-block">ID: {{ student.id }}</small>
          </div>
          <span class="badge bg-primary">{{ student.grades?.length || 0 }} calificaciones</span>
        </div>
        <div class="card-body p-0">
          <table class="table mb-0 table-striped align-middle">
            <thead class="table-light">
              <tr>
                <th style="width: 70%">Curso</th>
                <th class="text-end">Nota</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(grade, idx) in student.grades" :key="idx">
                <td>{{ grade.course_name }}</td>
                <td class="text-end fw-semibold">{{ grade.score }}</td>
              </tr>
              <tr v-if="!student.grades || student.grades.length === 0">
                <td colspan="2" class="text-center text-muted py-3">Sin calificaciones registradas.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>
