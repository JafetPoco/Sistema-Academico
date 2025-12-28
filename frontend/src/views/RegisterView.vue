<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import authService from '../services/authService'

const full_name = ref('')
const email = ref('')
const password = ref('')
const confirm_password = ref('')
const loading = ref(false)
const message = ref(null)
const router = useRouter()

async function submit() {
  message.value = null
  loading.value = true
  try {
    const data = await authService.register(full_name.value, email.value, password.value, confirm_password.value)
    if (data?.status === 'success') {
      // show success and redirect to login
      router.push('/login')
      return
    }
    message.value = { type: 'error', text: data?.message || 'Error en el registro' }
  } catch (err) {
    console.error(err)
    message.value = { type: 'error', text: err.message || 'Error conectando al servidor.' }
  } finally {
    loading.value = false
  }
}
</script>

<template>
    <div class="bg">
        <div class="container d-flex justify-content-center align-items-center vh-100">
          <div class="col-md-4">
            <div class="form-wrapper">
              <h2 class="card-title text-center mb-4">Registro</h2>
      
              <div v-if="message" :class="['alert', message.type === 'error' ? 'alert-danger' : 'alert-success']">
                {{ message.text }}
              </div>
      
              <form @submit.prevent="submit">
                <div class="mb-3">
                  <label for="full_name" class="form-label">Nombre completo</label>
                  <input v-model="full_name" type="text" id="full_name" name="full_name" class="form-control" required />
                </div>
                <div class="mb-3">
                  <label for="email" class="form-label">Correo electrónico</label>
                  <input v-model="email" type="email" id="email" name="email" class="form-control" required />
                </div>
                <div class="mb-3">
                  <label for="password" class="form-label">Contraseña</label>
                  <input v-model="password" type="password" id="password" name="password" class="form-control" required />
                </div>
                <div class="mb-3">
                  <label for="confirm_password" class="form-label">Confirmar contraseña</label>
                  <input v-model="confirm_password" type="password" id="confirm_password" name="confirm_password" class="form-control" required />
                </div>
                <div class="d-grid">
                  <button :disabled="loading" type="submit" class="btn btn-success">{{ loading ? 'Registrando...' : 'Registrar' }}</button>
                </div>
              </form>
      
              <p class="mt-3 text-center">
                ¿Ya tienes cuenta?
                <router-link to="/login">Inicia sesión</router-link>
              </p>
            </div>
          </div>
        </div>

    </div>
</template>

<style scoped>
.bg {
  background-image: url("../assets/img/background.jpg") !important;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.form-wrapper {
  background-color: rgba(255, 255, 255, 0.95);
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 0 25px rgba(0, 0, 0, 0.08);
  width: 100%;
}
.vh-100 { min-height: 100vh; }
</style>
