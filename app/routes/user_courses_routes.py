# app//routes/user_courses_routes.py

from flask import Blueprint, session, redirect, url_for
from app.application.user_courses_controller import CoursesController

courses_bp = Blueprint('courses', __name__, url_prefix='/cursos')
controller = CoursesController()

@courses_bp.route('/dashboard', methods=['GET'])
def dashboard():
    return controller.show_dashboard()

@courses_bp.route('/curso/<int:curso_id>', methods=['GET'])
def curso_page(curso_id):
    return controller.show_course_detail(curso_id)