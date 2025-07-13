#!/usr/bin/python
# -*- coding: utf-8 -*-
from database.db import db
class Curso(db.Model):
    __tablename__ = 'cursos'

    curso_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    
    def agregar_estudiante(self, estudiante):
        # Aquí luego podrías manejar la relación muchos-a-muchos con estudiantes
        pass

    def calcular_promedio(self):
        # Aquí podrías calcular un promedio de calificaciones si está relacionado
        pass
