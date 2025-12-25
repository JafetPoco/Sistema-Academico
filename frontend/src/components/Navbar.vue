<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const isAuthenticated = ref(false)
const user = ref(null)

async function checkAuth() {
    try {
        const res = await fetch('/api/auth/me', { credentials: 'include' })
        if (res.ok) {
            user.value = await res.json()
            isAuthenticated.value = true
        } else {
            isAuthenticated.value = false
        }
    } catch (e) {
        isAuthenticated.value = false
    }
}

const router = useRouter()
function navigate(href) {
    router.push(href)
}

async function logout() {
    try {
        await fetch('/api/auth/logout', { method: 'POST', credentials: 'include' })
    } catch (e) {
        // ignore
    }
    window.location.href = '/'
}

onMounted(() => {
    checkAuth()
})
</script>

<template>
    <div class="container-fluid">
        <nav class="navbar navbar-expand-lg bg-body-tertiary fixed-top">
            <div class="container-fluid">
                <span class="logo navbar-brand mb-0 h1" style="cursor:pointer" @click.prevent="navigate('/')">EDUNET</span>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                    <div class="navbar-nav ms-auto d-flex align-items-center gap-2">
                        <router-link class="nav-link active" aria-current="page" to="/" id="btn-home">Home</router-link>
                        <router-link class="nav-link active" to="/anuncios" id="btn-anuncios">Anuncios</router-link>

                        <template v-if="isAuthenticated">
                            <router-link class="nav-link active" to="/profile" id="btn-mi-perfil">Mi perfil</router-link>
                            <router-link class="nav-link active" to="/dashboard">Dashboard</router-link>
                        </template>
                        <template v-else>
                            <router-link class="nav-link active" to="/login">Dashboard</router-link>
                        </template>

                        <template v-if="isAuthenticated">
                            <button class="btn btn-dark" id="btn-logout" @click="logout">Logout</button>
                        </template>
                        <template v-else>
                            <router-link to="/login" class="btn btn-dark" id="btn-iniciar-sesion">Iniciar Sesión</router-link>
                        </template>
                    </div>
                </div>
            </div>
        </nav>
    </div>
</template>

<style scoped>
.logo { font-weight: 700; }
</style>