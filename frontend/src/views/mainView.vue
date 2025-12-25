<script setup>
import Navbar from '../components/Navbar.vue'
</script>

<template>
    <div>
        <Navbar />

        <div class="container pt-5">
            <h1 class="mt-5">EDUNET</h1>
            <p class="long-text">
                Tu espacio escolar digital.
                <br />
                Consulta tus notas, recibe anuncios importantes, mantente al día con tus actividades académicas y mucho más, todo desde un solo lugar. Pensado para estudiantes, padres y docentes, EDUNET conecta a toda la comunidad educativa de forma simple, rápida y segura
            </p>
        </div>

        <div class="container-fluid p-0 mt-5 mb-5">
            <img class="main-img" src="/img/img2.jpg" alt="EDUNET" />
        </div>

        <div class="container">
            <h2 class="mb-5">¿Qué ofrecemos?</h2>
            <div class="row">
                <div class="col">
                    <div>
                        <img class="secondary-img" src="/img/teacher.jpg" alt="teacher" />
                        <h4 class="mt-2">Comunicación directa con tus profesores</h4>
                        <p class="long-text">Mantente en contacto de forma rápida y sencilla. Podrás resolver dudas, recibir orientación personalizada y mantener un seguimiento constante de tu desempeño académico.</p>
                    </div>
                </div>
                <div class="col">
                    <div>
                        <img class="secondary-img" src="/img/schedule.jpg" alt="schedule" />
                        <h4 class="mt-2">Acceso inmediato a todas las novedades</h4>
                        <p class="long-text">No te pierdas nada importante. Infórmate al instante sobre comunicados oficiales, actividades escolares, fechas clave y noticias relevantes del colegio.</p>
                    </div>
                </div>
                <div class="col">
                    <div>
                        <img class="secondary-img" src="/img/feedback.jpg" alt="feedback" />
                        <h4 class="mt-2">Feedback personalizado</h4>
                        <p class="long-text">Recibe devoluciones y comentarios de tus profesores sobre tus trabajos, exámenes y participación. Una herramienta clave para mejorar tu aprendizaje y avanzar con seguridad.</p>
                    </div>
                </div>
            </div>
        </div>

        <footer>
            <div class="container d-flex justify-content-center">
                <div class="icons">
                    <i class="bi bi-facebook"></i>
                    <i class="bi bi-youtube"></i>
                    <i class="bi bi-instagram"></i>
                </div>
            </div>
        </footer>
    </div>
</template>

<style scoped>
.logo {
    font-size: 5vh;
}

.btn {
    font-size: 2.3vh;
    padding: 0.5vh 1w;
}

.long-text {
    margin: 20px 0;
    text-align: justify;
    font-weight: 200;
    font-size: vh;
}

.main-img {
    width: 100%;
    height: 88vh;
    object-fit: cover;
    display: block;
}

.secondary-img {
    width: 100%;
    height: 55vh;
    object-fit: cover;
    display: block;

    border-radius: 2%;
}

footer {
    background-color: rgb(229, 229, 229);
}

.icons {
    color: rgb(43, 43, 43);
    font-size: 20px;
    display: flex;
    padding: 8vh 0;
    gap: 20px;
}
</style>
