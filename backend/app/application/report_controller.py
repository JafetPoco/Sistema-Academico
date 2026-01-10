from app.infrastructure.repository.repository import CourseRepository
from app.domain.services.report_service import ReportService
from app.domain.services.course_service import CourseService


class ReportController:
    def __init__(self):
        self.course_repository = CourseRepository()
        self.course_service = CourseService(self.course_repository)
        self.report_service = ReportService()

    def list_professor_courses(self, professor_id: int) -> dict:
        if not professor_id:
            return {"success": False, "message": "Sesión inválida."}
        courses = self.course_service.get_courses_by_professor(professor_id)
        return {"success": True, "courses": courses or []}

    def course_report(self, course_id: int) -> dict:
        if not course_id:
            return {"success": False, "message": "course_id requerido."}
        course_grades, _ = self.report_service.get_course_grades(course_id)
        course_name = self.course_repository.get_course_name_by_id(course_id)
        return {"success": True, "course_name": course_name, "grades": course_grades or []}