from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import SQLAlchemyError
from app.infrastructure.database import get_session
from domain.entities import curso


MOSTRAR_CURSOS = 'curso.mostrar_cursos'

curso_bp = Blueprint('curso', __name__)
repositorio = CursoRepositorioImpl()

@curso_bp.route('/cursos', methods=['GET'])
def mostrar_cursos():
    session = get_session()
    try:
        cursos = repositorio.obtener_todos(session)
    except SQLAlchemyError:
        flash("Ocurrió un error al cargar los cursos.", "danger")
        cursos = []
    return render_template('cursos/cursos.html', cursos=cursos)

@curso_bp.route('/cursos', methods=['POST'])
def crear_curso():
    session = get_session()
    nombre = request.form.get('nombre', '').strip()

    if not nombre:
        flash("El nombre del curso no puede estar vacío.", "warning")
        return redirect(url_for(MOSTRAR_CURSOS))

    nuevo_curso = curso(nombre=nombre)
    try:
        repositorio.agregar(session, nuevo_curso)
        flash("Curso creado exitosamente.", "success")
    except SQLAlchemyError:
        flash("Error al crear el curso. Intente más tarde.", "danger")

    return redirect(url_for(MOSTRAR_CURSOS))

@curso_bp.route('/cursos/eliminar/<int:curso_id>', methods=['POST'])
def eliminar_curso(curso_id):
    session = get_session()
    try:
        curso = repositorio.obtener(session, curso_id)
        if curso:
            repositorio.eliminar(session, curso_id)
            flash("Curso eliminado correctamente.", "success")
        else:
            flash("Curso no encontrado.", "warning")
    except SQLAlchemyError:
        flash("Error al eliminar el curso.", "danger")

    return redirect(url_for(MOSTRAR_CURSOS))

@curso_bp.route('/cursos/<int:curso_id>', methods=['GET'])
def detalle_curso(curso_id):
    session = get_session()
    curso = repositorio.obtener(session, curso_id)
    if not curso:
        flash("Curso no encontrado.", "warning")
        return redirect(url_for(MOSTRAR_CURSOS))
    
    return render_template('cursos/detalle_curso.html', curso=curso)
