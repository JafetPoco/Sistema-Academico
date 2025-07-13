#!/usr/bin/python
# -*- coding: utf-8 -*-

import uuid
from models.Notas.calificacion import Calificacion
from models.Notas.estudiante import Estudiante
from models.Usuarios.usuario import Usuario
from models.Notas.curso import Curso
from domain.models.base import Base


class profesor(Base):

    tablename = 'profesores'
    profesor_id = Column(Integer,ForeignKey('usuarios.usuario_id'), primary_key=True)

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
