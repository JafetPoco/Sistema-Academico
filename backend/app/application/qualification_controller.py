from app.infrastructure.repository.repository import GradeRepository
from app.domain.services.enrollment_service import EnrollmentService
from app.domain.services.calificacion_service import CalificacionService


class QualificationController:
    def __init__(self):
        self.enrollment_service = EnrollmentService()
        self.grade_repository = GradeRepository()
        self.calificacion_service = CalificacionService(self.grade_repository)

    def list_courses(self, professor_id: int) -> dict:
        if not professor_id:
            return {"success": False, "message": "Sesión inválida."}

        courses, error = self.enrollment_service.get_professor_courses(professor_id)
        if error:
            return {"success": False, "message": error, "courses": []}

        if not courses:
            return {"success": True, "message": "No tienes cursos asignados.", "courses": []}

        return {"success": True, "courses": courses}

    def get_students_for_course(self, professor_id: int, course_id: int) -> tuple[dict, int]:
        if not professor_id or not course_id:
            return ({"error": "Parámetros faltantes."}, 400)

        has_access, error = self.enrollment_service.validate_professor_course_access(
            professor_id, course_id
        )

        if not has_access:
            return ({"error": error or "No tienes acceso a este curso."}, 403)

        students, fetch_error = self.enrollment_service.get_students_enrolled_in_course(course_id)
        if fetch_error:
            return ({"error": fetch_error}, 500)

        if not students:
            return ({"students": [], "message": "No hay estudiantes matriculados."}, 200)

        return ({"students": students}, 200)

    def create_qualification(self, professor_id: int, student_id: int, course_id: int, score: float) -> tuple[dict, int]:
        validation_error = self._validate_ids(student_id, course_id) or self._parse_and_validate_score(score)
        if validation_error:
            return ({"error": validation_error}, 400)

        has_access, error = self.enrollment_service.validate_professor_course_access(
            professor_id, course_id
        )
        if not has_access:
            return ({"error": error or "No tienes permisos para calificar."}, 403)

        is_enrolled = self.enrollment_service.enrollment_repo.is_user_enrolled(student_id, course_id)
        if not is_enrolled:
            return ({"error": "El estudiante no está matriculado en este curso."}, 400)

        grade_data = {'student_id': student_id, 'course_id': course_id, 'score': float(score)}

        try:
            self.calificacion_service.calificate_student(grade_data)
            return ({"message": "Calificación registrada exitosamente."}, 201)
        except Exception as e:
            return ({"error": f"Error interno del servidor: {str(e)}"}, 500)

    @staticmethod
    def _parse_and_validate_score(score_value: float) -> str | None:
        try:
            score = float(score_value)
        except (TypeError, ValueError):
            return "El campo 'score' debe ser un número válido."
        if not (0 <= score <= 20):
            return "La calificación debe estar entre 0 y 20."
        return None

    @staticmethod
    def _validate_ids(student_id: int, course_id: int) -> str | None:
        try:
            int(student_id)
            int(course_id)
        except (TypeError, ValueError):
            return "Los IDs deben ser números válidos."
        return None