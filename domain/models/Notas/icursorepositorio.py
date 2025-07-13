#!/usr/bin/python
# -*- coding: utf-8 -*-

# domain/models/Notas/icursorepositorio.py
from abc import ABC, abstractmethod

class ICursoRepositorio:
    @abstractmethod
    def obtener(self, id):
        pass

    @abstractmethod
    def agregar(self, curso):
        pass

    @abstractmethod    
    def actualizar(self, curso):
        pass

    @abstractmethod
    def eliminar(self, id):
        pass
