from unittest.mock import patch

from app.domain.services.report_service import ReportService


def test_get_course_grades_builds_report():
    with patch("app.domain.services.report_service.GradeRepository") as repo_cls:
        repo = repo_cls.return_value
        repo.get_scores_with_student_names_by_course.return_value = [
            (18, 1, "Ana"),
            (12, 2, "Luis"),
        ]
        service = ReportService()
        service.grade_repo = repo

        report, error = service.get_course_grades(5)

    assert error is None
    assert report == [
        {"student_name": "Ana", "student_id": 1, "score": 18},
        {"student_name": "Luis", "student_id": 2, "score": 12},
    ]