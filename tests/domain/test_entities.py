import pytest

from app.domain.entities import Course, Grade, Professor, Student, Parent


def test_course_calculate_average_handles_empty_grades():
    course = Course(course_id=1, name="Matematicas", professor_id=10)

    assert course.calculate_average() is None

    course.add_grade(Grade(grade_id="g1", student_id=100, course_id=1, score=18))
    course.add_grade(Grade(grade_id="g2", student_id=101, course_id=1, score=14))

    assert course.calculate_average() == pytest.approx(16.0)


def test_professor_grade_student_assigns_grade_and_updates_collections():
    professor = Professor(professor_id=7)
    course = Course(course_id=1, name="Historia", professor_id=7)
    professor.courses.append(course)
    student = Student(user_id=55, parent_id=1)

    grade = professor.grade_student(student, course, score=19)

    assert grade.score == 19
    assert course.grades[0] is grade
    assert student.grades[0] is grade


def test_professor_grade_student_raises_when_course_not_owned():
    professor = Professor(professor_id=7)
    course = Course(course_id=1, name="Historia", professor_id=7)
    student = Student(user_id=55, parent_id=1)

    with pytest.raises(ValueError):
        professor.grade_student(student, course, score=10)


def test_parent_view_grades_delegates_to_service():
    class StubGradeService:
        def __init__(self):
            self.calls = []

        def get_by_student(self, student_id):
            self.calls.append(student_id)
            return [20, 18]

    parent = Parent(parent_id=1)
    stub_service = StubGradeService()

    result = parent.view_grades(stub_service, student_id=42)

    assert result == [20, 18]
    assert stub_service.calls == [42]
