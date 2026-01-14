<script setup>
import { ref, watch, onMounted } from 'vue'
import Navbar from '../components/Navbar.vue'
import qualificationService from '../services/qualificationService'

const courses = ref([])
const students = ref([])
const selectedCourse = ref('')
const selectedStudent = ref('')
const score = ref('')
const loading = ref(false)
const message = ref(null)

async function loadCourses() {
  loading.value = true
  message.value = null
  try {
    const res = await qualificationService.getCourses()
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

async function loadStudents(courseId) {
  if (!courseId) return
  loading.value = true
  students.value = []
  selectedStudent.value = ''
  try {
    const res = await qualificationService.getStudentsByCourse(courseId)
    if (res?.students) {
      students.value = res.students
    } else if (res?.error) {
      message.value = { type: 'error', text: res.error }
    }
  } catch (err) {
    message.value = { type: 'error', text: err.message || 'Error cargando estudiantes.' }
  } finally {
    loading.value = false
  }
}

async function submit() {
  if (!selectedCourse.value || !selectedStudent.value || !score.value) {
    message.value = { type: 'error', text: 'Selecciona curso, estudiante y nota.' }
    return
  }
  loading.value = true
  message.value = null
  try {
    const payload = {
      course_id: selectedCourse.value,
      student_id: selectedStudent.value,
      score: score.value,
    }
    const res = await qualificationService.submitQualification(payload)
    if (res?.message) {
      message.value = { type: 'success', text: res.message }
      score.value = ''
    } else if (res?.error) {
      message.value = { type: 'error', text: res.error }
    }
  } catch (err) {
    message.value = { type: 'error', text: err.message || 'Error enviando calificación.' }
  } finally {
    loading.value = false
  }
}

watch(selectedCourse, (val) => loadStudents(val))
onMounted(loadCourses)
</script>

<template>
  <Navbar />
  <div class="container pt-5">
    <div class="d-flex justify-content-between align-items-center mt-4 mb-3">
      <h2 class="mb-0"><i class="bi bi-journal-check text-success me-2"></i> Calificar estudiantes</h2>
      <button class="btn btn-outline-secondary btn-sm" @click="loadCourses" :disabled="loading">
        <i class="bi bi-arrow-clockwise me-1"></i> Recargar
      </button>
    </div>

    <div v-if="message" :class="['alert', message.type === 'error' ? 'alert-danger' : 'alert-success']">{{ message.text }}</div>

    <div class="card shadow-sm">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-4">
            <label class="form-label">Curso</label>
            <select v-model="selectedCourse" class="form-select" :disabled="loading || !courses.length">
              <option value="">Selecciona un curso</option>
              <option v-for="course in courses" :key="course.id" :value="course.id">{{ course.name }}</option>
            </select>
            <small v-if="!courses.length" class="text-muted">No tienes cursos asignados.</small>
          </div>
          <div class="col-md-4">
            <label class="form-label">Estudiante</label>
            <select v-model="selectedStudent" class="form-select" :disabled="loading || !students.length">
              <option value="">Selecciona un estudiante</option>
              <option v-for="stu in students" :key="stu.id" :value="stu.id">{{ stu.name }}</option>
            </select>
            <small v-if="selectedCourse && !students.length" class="text-muted">Sin estudiantes matriculados.</small>
          </div>
          <div class="col-md-4">
            <label class="form-label">Nota (0-20)</label>
            <input v-model="score" type="number" step="0.1" min="0" max="20" class="form-control" :disabled="loading" />
          </div>
        </div>

        <div class="mt-4 text-end">
          <button class="btn btn-primary" :disabled="loading" @click="submit">
            <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"></span>
            Guardar calificación
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
