<script>
import axios from 'axios'
import DashboardHeader from '../components/DashboardHeader.vue'
import AdminContent from '../components/AdminContent.vue'
import ParentContent from '../components/ParentContent.vue'
import TeacherContent from '../components/TeacherContent.vue'
import UnknownContent from '../components/unknownContent.vue'
const DefaultContent = { template: '<div><p>Contenido por defecto.</p></div>' }

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
            // Pass dashboardData only when available (ParentContent expects it)
            if (this.userRole === 3) return { dashboardData: this.dashboardData }
            return {}
        }
        ,
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
            try {
                // Fetch current user info; adjust endpoint to your backend
                let me = null
                try {
                    const meRes = await axios.get('/api/auth/me', { withCredentials: true })
                    me = meRes.data || {}
                    console.debug('/api/auth/me ->', meRes.status, me)
                } catch (e) {
                    // If /api/auth/me is not available (404) try fallback to localStorage (set by LoginView)
                    if (e.response && e.response.status === 404) {
                        console.warn('/api/auth/me returned 404, attempting localStorage fallback')
                        const stored = localStorage.getItem('user')
                        if (stored) {
                            try { me = JSON.parse(stored) } catch (er) { me = null }
                        }
                    } else {
                        throw e
                    }
                }

                if (!me) {
                    // no user info available
                    this.userName = null
                    this.userRole = null
                    this.roleName = null
                    throw new Error('No se encontró información del usuario (ni /api/auth/me ni localStorage).')
                }

                this.userName = me.full_name || me.name || me.fullName || 'Usuario'
                this.userRole = typeof me.role !== 'undefined' ? me.role : (me.role_id ?? me.roleId ?? 2)
                this.roleName = me.role_name || me.roleName || 'Usuario'

                // Fetch dashboard data depending on role. Adjust endpoints as needed.
                if (this.userRole === 3) {
                    const dashRes = await axios.get('/api/dashboard/parent', { withCredentials: true }).catch(err => { console.warn('parent dashboard fetch failed', err); return { data: null } })
                    this.dashboardData = dashRes.data
                } else if (this.userRole === 2) {
                    // admin dashboard could fetch admin stats if available
                    const dashRes = await axios.get('/api/dashboard/admin', { withCredentials: true }).catch(err => { console.warn('admin dashboard fetch failed', err); return { data: null } })
                    this.dashboardData = dashRes.data
                } else {
                    this.dashboardData = null
                }
            } catch (err) {
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
                <component :is="roleComponent" v-bind="componentProps" />
            </div>
        </div>
    </div>
</template>

<style scoped>
.container { max-width: 1100px; }
</style>