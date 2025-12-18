from typing import Optional

from app.infrastructure.repository.repository import (
    ParentRepository, EnrollmentRepository, GradeRepository, UserRepository
)
import logging

class ChildMetricsBuilder:
    def __init__(self, enrollment_repo: EnrollmentRepository, grade_repo: GradeRepository):
        self.enrollment_repo = enrollment_repo
        self.grade_repo = grade_repo

    def build(self, child) -> dict:
        child_id, child_name = self._extract_child_info(child)
        courses_count = self._get_courses_count(child_id)
        all_grades = self._safe_get_child_all_grades(child_id)
        return self._calculate_child_stats(child_id, child_name, courses_count, all_grades)

    def _extract_child_info(self, child):
        try:
            if isinstance(child, dict):
                return child.get('id', 0), child.get('name', 'Desconocido')
            return getattr(child, 'id', 0), getattr(child, 'name', 'Desconocido')
        except Exception:
            return 0, 'Error'

    def _get_courses_count(self, child_id):
        try:
            enrolled_courses, error = self.enrollment_repo.get_user_courses_with_names(child_id)
            return len(enrolled_courses) if not error and enrolled_courses else 0
        except Exception:
            return 0

    def _safe_get_child_all_grades(self, child_id):
        try:
            return self._get_child_all_grades(child_id)
        except Exception:
            return []

    def _calculate_child_stats(self, child_id, child_name, courses_count, all_grades):
        try:
            average_grade = self._calculate_average_grade(all_grades)
            courses_passed = self._count_passed_courses(all_grades)
            courses_failed = self._count_failed_courses(all_grades)
            highest_grade = max(all_grades) if all_grades else 0
            lowest_grade = min(all_grades) if all_grades else 0
            status = 'success'
        except Exception:
            average_grade = 0.0
            courses_passed = 0
            courses_failed = 0
            highest_grade = 0
            lowest_grade = 0
            status = 'error'
        return {
            'child_id': child_id,
            'child_name': child_name,
            'courses_enrolled': courses_count,
            'total_grades': len(all_grades),
            'average_grade': average_grade,
            'courses_passed': courses_passed,
            'courses_failed': courses_failed,
            'highest_grade': highest_grade,
            'lowest_grade': lowest_grade,
            'status': status
        }

    def _get_child_all_grades(self, child_id: int) -> list:
        try:
            grades, error = self.grade_repo.get_grades_by_student(child_id)

            if error or not grades:
                return []

            scores = []

            for grade in grades:
                try:
                    if isinstance(grade, dict):
                        score = grade.get('score', 0)
                    elif hasattr(grade, 'score'):
                        score = grade.score
                    else:
                        continue

                    if score > 0:
                        scores.append(score)

                except Exception:
                    continue

            return scores

        except Exception:
            return []

    def _calculate_average_grade(self, grades: list) -> float:
        if not grades:
            return 0.0

        try:
            return round(sum(grades) / len(grades), 2)
        except Exception:
            return 0.0

    def _count_passed_courses(self, grades: list) -> int:
        if not grades:
            return 0
        return len([grade for grade in grades if grade >= 11])

    def _count_failed_courses(self, grades: list) -> int:
        if not grades:
            return 0
        return len([grade for grade in grades if grade < 11])


class ParentDashboardService:  
    def __init__(
        self,
        parent_repo: Optional[ParentRepository] = None,
        enrollment_repo: Optional[EnrollmentRepository] = None,
        grade_repo: Optional[GradeRepository] = None,
        user_repo: Optional[UserRepository] = None,
    ):
        # Allow injecting repositories so the service can be tested with mocks
        self.parent_repo = parent_repo or ParentRepository()
        self.enrollment_repo = enrollment_repo or EnrollmentRepository()
        self.grade_repo = grade_repo or GradeRepository()
        self.user_repo = user_repo or UserRepository()
        self.metrics_builder = ChildMetricsBuilder(self.enrollment_repo, self.grade_repo)
    
    def get_parent_dashboard_data(self, parent_id: int) -> dict:
        try:
            children, error = self.parent_repo.get_children_by_parent(parent_id)
            guard = self._guard_children(children, error)
            if guard:
                return guard

            children_stats = []
            total_summary = self._initialize_total_summary()

            for child in children:
                child_stats = self.metrics_builder.build(child)
                children_stats.append(child_stats)
                self._accumulate_total_stats(total_summary, child_stats)

            self._finalize_total_summary(total_summary)

            return self._success_response(children_stats, total_summary, len(children))
            
        except Exception as e:
            logging.error(f"Error en get_parent_dashboard_data: {e}")
            return self._error_response(f"Error obteniendo datos: {str(e)}")

    def _guard_children(self, children, error):
        if error:
            return self._error_response(error)
        if not children:
            return {
                'children_stats': [],
                'total_summary': self._get_empty_summary(),
                'status': 'no_children',
                'message': 'No tienes hijos registrados en el sistema'
            }
        return None

    def _success_response(self, children_stats, total_summary, total_children):
        return {
            'children_stats': children_stats,
            'total_summary': total_summary,
            'total_children': total_children,
            'status': 'success'
        }

    def _error_response(self, message: str):
        return {
            'children_stats': [],
            'total_summary': self._get_empty_summary(),
            'status': 'error',
            'message': message
        }
    
    def _initialize_total_summary(self) -> dict:
        return {
            'total_courses': 0,
            'total_grades': 0,
            'total_passed': 0,
            'total_failed': 0,
            'overall_average': 0.0,
            'all_grades_sum': 0.0,
            'grades_count': 0
        }
    
    def _accumulate_total_stats(self, total_summary: dict, child_stats: dict):
        total_summary['total_courses'] += child_stats['courses_enrolled']
        total_summary['total_grades'] += child_stats['total_grades']
        total_summary['total_passed'] += child_stats['courses_passed']
        total_summary['total_failed'] += child_stats['courses_failed']
        
        if child_stats['total_grades'] > 0:
            child_total_score = child_stats['average_grade'] * child_stats['total_grades']
            total_summary['all_grades_sum'] += child_total_score
            total_summary['grades_count'] += child_stats['total_grades']
    
    def _finalize_total_summary(self, total_summary: dict):
        if total_summary['grades_count'] > 0:
            total_summary['overall_average'] = round(
                total_summary['all_grades_sum'] / total_summary['grades_count'], 2
            )
    
    def _get_empty_summary(self) -> dict:
        return {
            'total_courses': 0,
            'total_grades': 0,
            'total_passed': 0,
            'total_failed': 0,
            'overall_average': 0.0
        }
