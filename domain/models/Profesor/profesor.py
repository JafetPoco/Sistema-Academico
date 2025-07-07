#!/usr/bin/python
# -*- coding: utf-8 -*-

import uuid
from models.Notas.calificacion import Calificacion
from models.Notas.estudiante import Estudiante
from models.Notas.curso import Curso

class Profesor:
    def __init__(self):
        self.profesor_id = None
        self.usuario_id = None

    def crear_anuncio(self, curso, anuncio):
        pass

    def calificar_alumno(self, estudiante, curso, puntaje):
         # (opcional) Validar si el profesor enseña ese curso
        if curso not in self.cursos:
            raise ValueError("Este profesor no dicta este curso.")

        # Crear una calificación
        calificacion = Calificacion(
            calificacion_id=str(uuid.uuid4()),
            estudiante_id=estudiante.estudiante_id,
            curso_id=curso.curso_id,
            puntaje=puntaje
        )

        # Registrar calificación en curso
        curso.registrar_calificacion(calificacion)

        # Registrar calificación en el estudiante (opcional)
        estudiante.recibir_calificacion(calificacion)
