#!/usr/bin/python
# -*- coding: utf-8 -*-

class Padre:
    def __init__(self):
        self.padre_id = None

    def agregar_estudiante(self, estudiante):
        pass

    def ver_calificaciones(self, estudiante_id, calificacion_service):
        return calificacion_service.obtener_calificaciones_por_estudiante(estudiante_id)
