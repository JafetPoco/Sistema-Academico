#!/usr/bin/python
# -*- coding: utf-8 -*-
class Usuario:
    def __init__(self):
        self.usuario_id = None
        self.nombres = None
        self.correo = None
        self.hash_contrasena = None

    def cambiar_contrasena(self, nuevo_hash):
        self.hash_contrasena = nuevo_hash
        print("Contraseña cambiada correctamente.")
