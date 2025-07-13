
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
from domain.models.base import Base
from sqlalchemy.orm import relationship
import uuid

class usuario(Base):
    __tablename__ = 'usuarios'

    usuario_id = Column(Integer, primary_key=True)
    nombres = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    hash_contrasena = Column(String(128), nullable=False)
    rol = Column(Integer, nullable=False)  

    def __init__(self):
        self.usuario_id = None
        self.nombres = None
        self.correo = None
        self.hash_contrasena = None
        self.rol = None

    def cambiar_contrasena(self, nuevo_hash):
        self.hash_contrasena = nuevo_hash
        print("Contraseña cambiada correctamente.")

class anuncio(Base):
    __tablename__ = 'anuncios'

    anuncio_id = Column(Integer, primary_key=True)
    curso_id = Column(Integer, ForeignKey('cursos.curso_id'), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.usuario_id'), nullable=False)
    titulo = Column(String(255), nullable=False)
    contenido = Column(Text, nullable=False)
    fecha_creado = Column(DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Anuncio(id={self.anuncio_id}, titulo='{self.titulo}')>"

class asistencia:
    def __init__(self):
        self.id = None
        self.estudiante_id = None
        self.curso_id = None

class calificacion(Base):
    __tablename__ = 'calificaciones'

    calificacion_id = Column(String(36), primary_key=True)
    estudiante_id = Column(Integer, ForeignKey('estudiantes.id'), nullable=False)
    curso_id = Column(Integer, ForeignKey('cursos.curso_id'), nullable=False)
    puntaje = Column(Integer, nullable=False)

    estudiante = relationship("estudiante", back_populates="calificaciones")
    curso = relationship("curso", back_populates="calificaciones")

class padre(Base):
    __tablename__ = 'padres'

    id = Column(Integer,ForeignKey('usuarios.usuario_id'), primary_key=True)

    estudiantes = relationship("estudiante", back_populates="padre")

    def agregar_estudiante(self, estudiante):
        pass

    def ver_calificaciones(self, estudiante_id, calificacion_service):
        return calificacion_service.obtener_calificaciones_por_estudiante(estudiante_id)

class curso(Base):
    __tablename__ = 'cursos'

    curso_id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    profesor_id = Column(Integer, ForeignKey('profesores.profesor_id'), nullable=False)

    profesor = relationship("profesor", back_populates="cursos")
    
    def agregar_estudiante(self, estudiante):
        # Aquí luego podrías manejar la relación muchos-a-muchos con estudiantes
        pass

    def calcular_promedio(self):
        # Aquí podrías calcular un promedio de calificaciones si está relacionado
        pass

class estudiante(Base):
    __tablename__ = 'estudiantes'

    id = Column(Integer, ForeignKey('usuarios.usuario_id'), primary_key=True)
    padre_id = Column(Integer, ForeignKey('padres.id'), nullable=True)

    padre = relationship("padre", back_populates="estudiantes")
    
    def agregar_padre(self, padre):
        if not isinstance(padre, padre):
            raise ValueError("El objeto proporcionado no es un padre válido.")
        self.padre_id = padre.id

class anuncio(Base):
    __tablename__ = 'anuncios'

    anuncio_id = Column(Integer, primary_key=True)
    curso_id = Column(Integer, ForeignKey('cursos.curso_id'), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.usuario_id'), nullable=False)
    titulo = Column(String(255), nullable=False)
    contenido = Column(Text, nullable=False)
    fecha_creado = Column(DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Anuncio(id={self.anuncio_id}, titulo='{self.titulo}')>"
    
class administrador(Base):
    __tablename__ = 'administradores'
    id = Column(Integer, ForeignKey('usuarios.usuario_id'), primary_key=True)

    def __init__(self):
        self.administrador_id = None
        self.usuario_id = None

    def crear_usuario(self, usuario):
        pass

    def eliminar_usuario(self, usuario):
        pass

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
