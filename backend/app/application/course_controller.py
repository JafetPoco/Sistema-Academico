from sqlalchemy.exc import SQLAlchemyError
from app.domain.services.enrollment_service import EnrollmentService

enrollment_service = EnrollmentService()


class CourseController:
    def __init__(self):
        self.service = EnrollmentService()

    def get_professor_courses(self, professor_id: int) -> dict:
        if not professor_id:
            return {"success": False, "message": "Profesor no autenticado."}

        try:
            info_courses, error = self.service.get_professor_courses_with_student_counts(professor_id)
            if error:
                return {"success": False, "message": error, "courses": []}
            return {"success": True, "courses": info_courses or []}
        except SQLAlchemyError as exc:
            return {"success": False, "message": f"Ocurrió un error al cargar los cursos: {str(exc)}", "courses": []}
