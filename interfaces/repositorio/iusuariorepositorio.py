#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

class IUsuarioRepositorio(ABC):
    @abstractmethod
    def obtener(self, id):
        pass

    @abstractmethod
    def agregar(self, usuario):
        pass

    @abstractmethod
    def actualizar(self, usuario):
        pass

    @abstractmethod
    def eliminar(self, id):
        pass