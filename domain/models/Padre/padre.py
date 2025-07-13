#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from domain.models.base import Base

class padre(Base):
    __tablename__ = 'padres'

    id = Column(Integer,ForeignKey('usuarios.usuario_id'), primary_key=True)

    estudiantes = relationship("estudiante", back_populates="padre")


    def agregar_estudiante(self, estudiante):
        pass

    def ver_calificaciones(self, estudiante):

        if not isinstance(estudiante, Estudiante):
            raise ValueError("El objeto proporcionado no es un estudiante válido.")
        
            
        for calificacion in estudiante.calificaciones:
            print(f"Curso: {calificacion.curso_id}, Puntaje: {calificacion.puntaje}")
        
        if not estudiante.calificaciones:       
            raise ValueError("El estudiante no tiene calificaciones registradas.")  
        pass
