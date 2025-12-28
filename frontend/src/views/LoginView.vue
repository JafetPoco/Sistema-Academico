<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import authService from '../services/authService'

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const router = useRouter()

async function submit() {
  error.value = ''
  loading.value = true
  try {
    const data = await authService.login(email.value, password.value)
    console.log(data)
    if (data?.status === 'success') {
      // store returned user info if present so dashboard can fallback when /api/auth/me is missing
      const userPayload = data.user || (data.data && data.data.user) || null
      if (userPayload) localStorage.setItem('user', JSON.stringify(userPayload))
      // also accept role directly in response
      if (!userPayload && data.role) localStorage.setItem('user', JSON.stringify({ role: data.role, role_name: data.role_name, full_name: data.full_name }))
      router.push('/dashboard')
      return
    }
    error.value = data?.message || 'Credenciales inválidas.'
  } catch (err) {
    console.error(err)
    error.value = err.message || 'Error conectando al servidor.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <div class="form-wrapper container-fluid">
      <h2 class="text-center mb-4">Iniciar Sesión</h2>

      <div v-if="error" class="alert alert-danger" role="alert">{{ error }}</div>

      <form @submit.prevent="submit">
        <div class="mb-3">
          <label for="email" class="form-label">Correo electrónico</label>
          <input v-model="email" type="email" id="email" name="email" class="form-control" required />
        </div>

        <div class="mb-3">
          <label for="password" class="form-label">Contraseña</label>
          <input v-model="password" type="password" id="password" name="password" class="form-control" required />
        </div>

        <button :disabled="loading" type="submit" class="btn btn-primary w-100" id="btn-login">
          {{ loading ? 'Entrando...' : 'Iniciar sesión' }}
        </button>
      </form>

      <p class="mt-3 text-center">
        ¿No tienes cuenta?
        <router-link to="/register" id="btn-registrate">Registrate</router-link>
      </p>
    </div>
  </div>
</template>



<style scoped>
.login-page {
  background-image: url("../assets/img/background.jpg") !important;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
.form-wrapper {
  background-color: rgba(255, 255, 255, 0.95);
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 0 25px rgba(0, 0, 0, 0.08);
  width: 100%;
  max-width: 420px;
}
</style>
