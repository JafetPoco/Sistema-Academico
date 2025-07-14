#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

class IProfesorRepositorio:
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def obtener(self, id):
        pass

    @abstractmethod
    def agregar(self, profesor):
        pass
    
    @abstractmethod
    def actualizar(self, profesor):
        pass
    
    @abstractmethod
    def eliminar(self, id):
        pass
