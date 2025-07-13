from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import SQLAlchemyError
from database.db import db
from domain.models.Notas.curso import Curso
from domain.repositories.mysql.curso_repositorio_impl import CursoRepositorioImpl



MOSTRAR_CURSOS = 'curso.mostrar_cursos'

curso_bp = Blueprint('curso', __name__)
repositorio = CursoRepositorioImpl()

@curso_bp.route('/cursos', methods=['GET'])
def mostrar_cursos():
    try:
        cursos = repositorio.obtener_todos(db.session)
    except SQLAlchemyError:
        flash("Ocurrió un error al cargar los cursos.", "danger")
        cursos = []
    return render_template('cursos/cursos.html', cursos=cursos)

@curso_bp.route('/cursos', methods=['POST'])
def crear_curso():
    nombre = request.form.get('nombre', '').strip()

    if not nombre:
        flash("El nombre del curso no puede estar vacío.", "warning")
        return redirect(url_for(MOSTRAR_CURSOS))

    nuevo_curso = Curso(nombre=nombre)
    try:
        repositorio.agregar(db.session, nuevo_curso)
        flash("Curso creado exitosamente.", "success")
    except SQLAlchemyError:
        flash("Error al crear el curso. Intente más tarde.", "danger")

    return redirect(url_for(MOSTRAR_CURSOS))

@curso_bp.route('/cursos/eliminar/<int:curso_id>', methods=['POST'])
def eliminar_curso(curso_id):
    try:
        curso = repositorio.obtener(db.session, curso_id)
        if curso:
            repositorio.eliminar(db.session, curso_id)
            flash("Curso eliminado correctamente.", "success")
        else:
            flash("Curso no encontrado.", "warning")
    except SQLAlchemyError:
        flash("Error al eliminar el curso.", "danger")

    return redirect(url_for(MOSTRAR_CURSOS))

@curso_bp.route('/cursos/<int:curso_id>', methods=['GET'])
def detalle_curso(curso_id):
    curso = repositorio.obtener(db.session, curso_id)
    if not curso:
        flash("Curso no encontrado.", "warning")
        return redirect(url_for(MOSTRAR_CURSOS))
    
    return render_template('cursos/detalle_curso.html', curso=curso)
