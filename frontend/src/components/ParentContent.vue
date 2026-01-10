<template>
    <div>
        <!-- Acciónes principales -->
        <div class="row g-4">
            <div class="col-md-6">
                <div class="card dashboard-card h-100 shadow-sm" id="card-calificaciones">
                    <div class="card-body text-center">
                        <div class="mb-3"><i class="bi bi-card-checklist fs-1 text-success"></i></div>
                        <h5 class="card-title" id="card-title-calificaciones">Ver Calificaciones</h5>
                        <p class="card-text">Ve todas las notas y calificaciones por curso</p>
                        <router-link to="/grades/parent" class="btn btn-success" id="btn-notas">Ver Notas</router-link>
                    </div>
                </div>
            </div>

            <div class="col-md-6">
                <div class="card dashboard-card h-100 shadow-sm" id="card-perfil">
                    <div class="card-body text-center">
                        <div class="mb-3"><i class="bi bi-person-fill fs-1 text-info"></i></div>
                        <h5 class="card-title" id="card-title-perfil">Mi Perfil</h5>
                        <p class="card-text">Actualiza tu información personal</p>
                        <router-link to="/profile" class="btn btn-info" id="btn-perfil">Ver Perfil</router-link>
                    </div>
                </div>
            </div>
        </div>

        <!-- Estados según dashboardData.status -->
        <div v-if="hasData && dashboardData.status === 'success'" class="mt-5">
            <div class="card mb-4">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <h5 class="mb-0">📊 Resumen General - Todos los Hijos</h5>
                    <small class="text-success"><i class="fas fa-users"></i> {{ dashboardData.total_children }} hijo(s)</small>
                </div>
                <div class="card-body">
                    <div class="row text-center">
                        <div class="col-md-3" v-for="(val, idx) in totalSummaryList" :key="idx">
                            <div class="stat-item">
                                <h4 :class="val.class">{{ val.value }}</h4>
                                <p class="text-muted">{{ val.label }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="card mb-4">
                <div class="card-header"><h5 class="mb-0">👶 Progreso Individual por Hijo</h5></div>
                <div class="card-body">
                    <div v-for="child in dashboardData.children_stats" :key="child.child_id" class="child-stats-card mb-4 p-3 border rounded bg-light">
                        <div class="row align-items-center mb-3">
                            <div class="col-md-8">
                                <h6 class="mb-1"><i class="fas fa-child text-primary"></i> <strong>{{ child.child_name }}</strong></h6>
                                <small class="text-muted">ID: {{ child.child_id }}</small>
                            </div>
                            <div class="col-md-4 text-end">
                                <span v-if="child.average_grade >= 15" class="badge bg-success">Excelente</span>
                                <span v-else-if="child.average_grade >= 11" class="badge bg-warning">Aprobado</span>
                                <span v-else-if="child.average_grade > 0" class="badge bg-danger">Necesita Apoyo</span>
                                <span v-else class="badge bg-secondary">Sin Calificaciones</span>
                            </div>
                        </div>

                        <div class="row text-center">
                            <div class="col-6 col-md-3"><div class="mini-stat"><h6 class="text-primary mb-1">{{ child.courses_enrolled }}</h6><small class="text-muted">Cursos</small></div></div>
                            <div class="col-6 col-md-3"><div class="mini-stat"><h6 class="text-success mb-1">{{ child.average_grade }}</h6><small class="text-muted">Promedio</small></div></div>
                            <div class="col-6 col-md-3"><div class="mini-stat"><h6 class="text-warning mb-1">{{ child.total_grades }}</h6><small class="text-muted">Calificaciones</small></div></div>
                            <div class="col-6 col-md-3"><div class="mini-stat"><h6 class="text-info mb-1">{{ child.courses_passed }}</h6><small class="text-muted">Aprobados</small></div></div>
                        </div>

                        <div v-if="child.total_grades > 0" class="row mt-3">
                            <div class="col-md-6"><small class="text-success"><i class="fas fa-arrow-up"></i> Nota más alta: {{ child.highest_grade }}</small></div>
                            <div class="col-md-6"><small class="text-danger"><i class="fas fa-arrow-down"></i> Nota más baja: {{ child.lowest_grade }}</small></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div v-else-if="hasData && dashboardData.status === 'no_children'" class="row mt-5">
            <div class="col-12">
                <div class="alert alert-info text-center">
                    <i class="fas fa-users fa-3x mb-3"></i>
                    <h5>No tienes hijos registrados</h5>
                    <p>Contacta al administrador para registrar a tus hijos en el sistema.</p>
                </div>
            </div>
        </div>

        <div v-else-if="hasData && dashboardData.status === 'error'" class="row mt-5">
            <div class="col-12">
                <div class="alert alert-danger text-center">
                    <i class="fas fa-exclamation-triangle fa-2x mb-3"></i>
                    <h5>Error cargando información</h5>
                    <p>{{ dashboardData.message }}</p>
                    <button class="btn btn-outline-danger" @click="reloadPage"><i class="fas fa-sync-alt"></i> Intentar de nuevo</button>
                </div>
            </div>
        </div>

        <div v-else class="row mt-5">
            <div class="col-12 text-center">
                <div class="spinner-border text-primary" role="status"><span class="visually-hidden">Cargando...</span></div>
                <p class="mt-2">Cargando información de tus hijos...</p>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ParentContent',
    props: {
        dashboardData: { type: Object, default: null }
    },
    methods: {
        reloadPage () { this.$emit('reload') },
        showChildrenModal () { alert('Funcionalidad de modal detallado por implementar') }
    },
    computed: {
        hasData () { return this.dashboardData !== null },
        totalSummaryList () {
            const s = this.dashboardData && this.dashboardData.total_summary ? this.dashboardData.total_summary : {}
            return [
                { label: 'Cursos Totales', value: s.total_courses ?? 0, class: 'text-primary' },
                { label: 'Promedio General', value: s.overall_average ?? 0, class: 'text-success' },
                { label: 'Total Calificaciones', value: s.total_grades ?? 0, class: 'text-warning' },
                { label: 'Cursos Aprobados', value: s.total_passed ?? 0, class: 'text-info' }
            ]
        }
    }
}
</script>

<style scoped>
.stat-item { padding: 1rem; }
.stat-item h4 { font-size: 2.5rem; font-weight: bold; margin-bottom: 0.5rem; }
.mini-stat h6 { font-size: 1.2rem; font-weight: bold; }
.child-stats-card { border-left: 4px solid #007bff !important; transition: all 0.3s ease; }
.child-stats-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.alert { border-radius: 15px; }
</style>