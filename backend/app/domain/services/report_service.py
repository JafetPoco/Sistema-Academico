from app.infrastructure.repository.repository import GradeRepository

class ReportService:
    def __init__(self):
        self.grade_repo = GradeRepository()

    def get_course_grades(self, course_id: int):
        grades_with_students = self.grade_repo.get_scores_with_student_names_by_course(course_id)
        
        report_data = []
        for score, student_id, full_name in grades_with_students:
            report_data.append({
                'student_name': full_name,
                'student_id': student_id,
                'score': score
            })
            
        return report_data, None

    