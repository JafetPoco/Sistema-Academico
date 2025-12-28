<template>
  <div>
    <Navbar />
    <div class="container mt-5 pt-5">
      <div class="mb-4 d-flex justify-content-between align-items-center">
        <div>
          <h1 class="mb-1">Administrar usuarios</h1>
        </div>
        <button class="btn btn-sm btn-outline-secondary" @click="loadUsers" :disabled="loading">
          Recargar
          <span v-if="loading" class="spinner-border spinner-border-sm ms-2" role="status" aria-hidden="true"></span>
        </button>
      </div>

    <div v-if="loading" class="alert alert-info">Cargando usuarios...</div>
    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else class="table-responsive shadow-sm rounded">
      <table class="table table-striped table-bordered mb-0">
        <thead class="table-dark">
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Correo Electrónico</th>
            <th>Rol</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.full_name }}</td>
            <td>{{ user.email }}</td>
            <td>
              <select
                class="form-select form-select-sm"
                v-model="selectedRoles[user.id]"
              >
                <option v-for="(label, value) in roleOptions" :key="value" :value="value">{{ label }}</option>
              </select>
            </td>
            <td>
              <button
                class="btn btn-sm btn-primary"
                :class="{ 'disabled': updating[user.id] }"
                :disabled="updating[user.id]"
                @click="updateRole(user.id)"
              >
                {{ updating[user.id] ? 'Actualizando…' : 'Actualizar' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    </div>
  </div>
</template>

<script setup>
import Navbar from '../components/Navbar.vue'
import { onMounted, reactive, ref } from 'vue'
import adminService from '../services/adminService'

const users = ref([])
const loading = ref(true)
const error = ref('')
const selectedRoles = reactive({})
const updating = reactive({})

const roleOptions = {
  '0': 'Inactivo',
  '1': 'Profesor',
  '2': 'Administrativo',
  '3': 'Padre',
}

function initializeRoles(payload) {
  (payload.data || []).forEach((user) => {
    selectedRoles[user.id] = String(user.role)
  })
}

async function loadUsers() {
  loading.value = true
  error.value = ''
  try {
    const payload = await adminService.fetchUsers()
    users.value = payload.data || []
    initializeRoles(payload)
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

async function updateRole(userId) {
  const role = selectedRoles[userId]
  if (role == null) {
    return
  }
  updating[userId] = true
  error.value = ''
  try {
    await adminService.updateUserRole(userId, role)
    await loadUsers()
  } catch (err) {
    error.value = `Error actualizando rol: ${err.message}`
  } finally {
    updating[userId] = false
  }
}

onMounted(loadUsers)
</script>
