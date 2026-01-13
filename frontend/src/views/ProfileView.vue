<template>
  <div>
    <Navbar />
    <div class="container pt-5">
      <div class="d-flex justify-content-between align-items-center mt-4 mb-3">
        <h2 class="mb-0"><i class="bi bi-person-circle text-primary me-2"></i> Mi Perfil</h2>
        <button class="btn btn-outline-secondary btn-sm" @click="loadProfile" :disabled="loading">
          <i class="bi bi-arrow-clockwise me-1"></i> Actualizar
        </button>
      </div>

      <div v-if="loading" class="text-center py-4">
        <div class="spinner-border text-primary" role="status"><span class="visually-hidden">Cargando...</span></div>
        <p class="mt-2">Cargando perfil...</p>
      </div>

      <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

      <div v-else-if="profile" class="row">
        <div class="col-md-8 mx-auto">
          <div class="card shadow-sm">
            <div class="card-body">
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label fw-bold">ID de Usuario</label>
                  <p class="form-control-plaintext">{{ profile.user_id }}</p>
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-bold">Nombre Completo</label>
                  <p class="form-control-plaintext">{{ profile.name }}</p>
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-bold">Correo Electrónico</label>
                  <p class="form-control-plaintext">{{ profile.email }}</p>
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-bold">Rol</label>
                  <p class="form-control-plaintext">{{ getRoleLabel(profile.role) }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="alert alert-warning">No se pudo cargar la información del perfil.</div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import Navbar from '../components/Navbar.vue'
import userService from '../services/userService'

const profile = ref(null)
const loading = ref(true)
const error = ref('')

const roleLabels = {
  0: 'Inactivo',
  1: 'Profesor',
  2: 'Administrador',
  3: 'Padre',
}

function getRoleLabel(role) {
  return roleLabels[role] || 'Desconocido'
}

async function loadProfile() {
  loading.value = true
  error.value = ''
  try {
    const data = await userService.fetchProfile()
    profile.value = data
  } catch (err) {
    error.value = err.message || 'Error cargando perfil.'
  } finally {
    loading.value = false
  }
}

onMounted(loadProfile)
</script>

<style scoped>
.card-body { padding: 2rem; }
.form-control-plaintext { border: none; background: none; padding: 0; }
</style>
