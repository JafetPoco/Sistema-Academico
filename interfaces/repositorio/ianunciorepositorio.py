#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

class ianuncio_repositorio(ABC):

    @abstractmethod
    def create(self, anuncio):
        pass

    @abstractmethod
    def get(self, id):
        pass

    @abstractmethod
    def update(self, anuncio):
        pass

    @abstractmethod
    def delete(self, id):
        pass
