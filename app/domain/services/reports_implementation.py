from domain.entities import Course, Grade
from infrastructure.repository.repository import GradeRepository, StudentRepository, CourseRepository
def get_course_grades_report(self, course_identifier: int):
    course = self._get_course_or_none(course_identifier)
    if not course:
        return None

    grades = self._get_grades_for_course(course_identifier)
    report_data = self._build_report_data(grades)

    return {
        "course_name": course.name,
        "professor_id": course.professor_id,
        "grades": report_data
    }

def _get_course_or_none(self, course_identifier: int):
    return self.course_repository.get(course_identifier)

def _get_grades_for_course(self, course_identifier: int):
    all_grades = self.grade_repository.list_all()
    return [grade for grade in all_grades if grade.course_id == course_identifier]

def _build_report_data(self, grades):
    report_data = []
    for grade in grades:
        student = self.student_repository.get(grade.student_id)
        report_data.append({
            "student_id": student.user_id,
            "score": grade.score
        })
    return report_data
