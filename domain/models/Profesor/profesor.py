#!/usr/bin/python
# -*- coding: utf-8 -*-

import uuid
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from domain.models.base import Base


class profesor(Base):

    __tablename__ = 'profesores'
    profesor_id = Column(Integer,ForeignKey('usuarios.usuario_id'), primary_key=True)

    cursos = relationship("curso", back_populates="profesor")

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
