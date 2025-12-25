from types import SimpleNamespace
from unittest.mock import Mock

from app.domain.services.parent_dashboard_service import ParentDashboardService


def test_get_parent_dashboard_data_successfully_aggregates_stats():
    parent_repo = Mock()
    enrollment_repo = Mock()
    grade_repo = Mock()

    parent_repo.get_children_by_parent.return_value = ([{"id": 1, "name": "Ana"}], None)
    enrollment_repo.get_user_courses_with_names.return_value = ([{"id": 10}, {"id": 11}], None)
    grade_repo.get_grades_by_student.return_value = (
        [SimpleNamespace(score=15), SimpleNamespace(score=8)],
        None,
    )

    service = ParentDashboardService(
        parent_repo=parent_repo,
        enrollment_repo=enrollment_repo,
        grade_repo=grade_repo,
    )

    result = service.get_parent_dashboard_data(parent_id=99)

    assert result["status"] == "success"
    assert result["total_children"] == 1
    assert result["children_stats"][0]["average_grade"] == 11.5
    assert result["children_stats"][0]["courses_passed"] == 1
    assert result["children_stats"][0]["courses_failed"] == 1
    assert result["total_summary"]["overall_average"] == 11.5

    parent_repo.get_children_by_parent.assert_called_once_with(99)
    enrollment_repo.get_user_courses_with_names.assert_called_once_with(1)
    grade_repo.get_grades_by_student.assert_called_once_with(1)


def test_get_parent_dashboard_data_handles_missing_children():
    parent_repo = Mock()
    enrollment_repo = Mock()
    grade_repo = Mock()

    parent_repo.get_children_by_parent.return_value = ([], None)

    service = ParentDashboardService(
        parent_repo=parent_repo,
        enrollment_repo=enrollment_repo,
        grade_repo=grade_repo,
    )

    result = service.get_parent_dashboard_data(parent_id=5)

    assert result["status"] == "no_children"
    assert result["total_summary"] == {
        "total_courses": 0,
        "total_grades": 0,
        "total_passed": 0,
        "total_failed": 0,
        "overall_average": 0.0,
    }


def test_get_parent_dashboard_data_propagates_repository_errors():
    parent_repo = Mock()
    enrollment_repo = Mock()
    grade_repo = Mock()

    parent_repo.get_children_by_parent.return_value = ([], "Database offline")

    service = ParentDashboardService(
        parent_repo=parent_repo,
        enrollment_repo=enrollment_repo,
        grade_repo=grade_repo,
    )

    result = service.get_parent_dashboard_data(parent_id=5)

    assert result["status"] == "error"
    assert result["message"] == "Database offline"