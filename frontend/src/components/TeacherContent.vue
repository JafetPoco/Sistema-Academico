<script>
export default {
    name: 'TeacherContent',
    data () {
        return {
            cards: [
                { id: 'calificar', title: 'Calificar Estudiantes', text: 'Asigna calificaciones a tus estudiantes', to: '/calificaciones/form', btnText: 'Calificar', btnClass: 'btn-success', icon: 'bi bi-journal-check', iconColor: 'text-success' },
                { id: 'cursos', title: 'Mis Cursos', text: 'Gestiona los cursos que enseñas', to: '/courses/professor', btnText: 'Ver Cursos', btnClass: 'btn-primary', icon: 'bi bi-mortarboard-fill', iconColor: 'text-primary' },
                { id: 'reportes', title: 'Reportes', text: 'Ve estadísticas de tus estudiantes', to: '/reportes', btnText: 'Ver Reportes', btnClass: 'btn-info', icon: 'bi bi-bar-chart', iconColor: 'text-info' }
            ]
        }
    }
}
</script>

<template>
    <div class="row g-4">
        <div class="col-md-4" v-for="card in cards" :key="card.id">
            <div class="card dashboard-card h-100 shadow-sm" :id="card.id">
                <div class="card-body text-center">
                    <div class="mb-3"><i :class="card.icon + ' fs-1 ' + card.iconColor"></i></div>
                    <h5 class="card-title" :id="`card-title-${card.id}`">{{ card.title }}</h5>
                    <p class="card-text">{{ card.text }}</p>
                    <router-link :to="card.to" class="btn" :class="card.btnClass">{{ card.btnText }}</router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.dashboard-card { border-radius: 10px; }
.card-title { margin-bottom: 0.5rem; }
.btn { margin-top: 0.8rem; }
</style>