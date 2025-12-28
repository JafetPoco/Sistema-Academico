# app/application/grades_controller.py
from app.domain.services.grade_service import GradeService

class GradesController:
    def __init__(self):
        self.grade_service = GradeService()

    def get_children_grades(self, parent_id):
        children_grades = self.grade_service.get_grades_by_parent_id(parent_id)
        if children_grades:
            return {'success': True, 'data': children_grades}
        else:
            return {'success': False, 'message': 'No se encontraron hijos o calificaciones.'}