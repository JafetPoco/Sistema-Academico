<script>
import axios from 'axios'
import DashboardHeader from '../components/DashboardHeader.vue'
import AdminContent from '../components/AdminContent.vue'
import ParentContent from '../components/ParentContent.vue'
import TeacherContent from '../components/TeacherContent.vue'
import UnknownContent from '../components/unknownContent.vue'

const DefaultContent = { template: '<div><p>Contenido por defecto.</p></div>' }
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5000'

export default {
    name: 'DashboardView',
    components: { DashboardHeader, AdminContent, ParentContent, TeacherContent, UnknownContent, DefaultContent },
    data () {
        return {
            userName: null,
            userRole: null,
            roleName: null,
            dashboardData: null,
            loading: false,
            error: null
        }
    },
    computed: {
        roleComponent () {
            switch (this.userRole) {
                case 0: return UnknownContent
                case 1: return TeacherContent
                case 2: return AdminContent
                case 3: return ParentContent
                default: return DefaultContent
            }
        },
        componentProps () {
            if (this.userRole === 3) return { dashboardData: this.dashboardData }
            return {}
        },
        errorMessage () {
            if (!this.error) return null
            return this.error.message || (this.error.response && (this.error.response.data?.message || JSON.stringify(this.error.response.data))) || String(this.error)
        }
    },
    created () {
        this.init()
    },
    methods: {
        handleLogout () {
            this.$router.push('/logout')
        },
        async init () {
            this.loading = true
            this.error = null
            try {
                const res = await axios.get(`${API_BASE}/dashboard/`, { withCredentials: true })
                const data = res.data || {}

                if (data.status !== 'success') {
                    throw new Error(data.message || 'No se pudo cargar el dashboard')
                }

                this.userName = data.user_name || data.name || 'Usuario'
                this.userRole = typeof data.user_role !== 'undefined' ? data.user_role : null
                this.roleName = data.role_name || data.role_display || 'Usuario'
                this.dashboardData = data.dashboard_data || null
            } catch (err) {
                // Fallback to localStorage if API is unreachable but session exists locally
                const stored = localStorage.getItem('user')
                if (stored && !this.userRole) {
                    try {
                        const parsed = JSON.parse(stored)
                        this.userName = parsed.full_name || parsed.name || 'Usuario'
                        this.userRole = parsed.role
                        this.roleName = parsed.role_name || parsed.roleName || 'Usuario'
                    } catch (e) {
                        // ignore
                    }
                }
                this.error = err
                console.error('Error cargando usuario/dashboard', err)
            } finally {
                this.loading = false
            }
        }
    }
}
</script>

<template>
    <div>
        <DashboardHeader
            :user-name="userName"
            :user-role="userRole"
            :role-name="roleName"
            @logout="handleLogout"
        />

        <div class="container mt-4">
            <div v-if="loading" class="text-center py-5">
                <div class="spinner-border text-primary" role="status"><span class="visually-hidden">Cargando...</span></div>
                <p class="mt-2">Cargando dashboard...</p>
            </div>

            <div v-else-if="error" class="py-4">
                <div class="alert alert-danger">
                    <strong>Error:</strong> {{ errorMessage }}
                    <div class="mt-2"><button class="btn btn-sm btn-secondary" @click="init">Reintentar</button></div>
                </div>
            </div>

            <div v-else-if="userRole === null" class="py-4">
                <div class="alert alert-warning">
                    No se pudo cargar la información del usuario. <button class="btn btn-sm btn-secondary" @click="init">Reintentar</button>
                </div>
            </div>

            <div v-else>
                <component :is="roleComponent" v-bind="componentProps" @reload="init" />
            </div>
        </div>
    </div>
</template>

<style scoped>
.container { max-width: 1100px; }
</style>