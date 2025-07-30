# domain/entities/entities.py

from datetime import datetime, timezone
from uuid import UUID

class User:
    def __init__(self, user_id, full_name, email,
                 password_hash, role):
        self.user_id = user_id
        self.full_name = full_name
        self.email = email
        self.password_hash = password_hash
        self.role = role

    def change_password(self, new_hash: str):
        self.password_hash = new_hash

    def __repr__(self):
        return f"<User(id={self.user_id}, email={self.email})>"

class Announcement:
    def __init__(self, announcement_id, course_id, user_id,
                 title, content, is_private, created_at):
        self.announcement_id = announcement_id
        self.course_id = course_id
        self.user_id = user_id
        self.title = title
        self.content = content
        self.is_private = is_private
        self.created_at = created_at or datetime.now(timezone.utc)

    def __repr__(self):
        return f"<Announcement(id={self.announcement_id}, title={self.title})>"

class Grade:
    def __init__(self, grade_id, student_id, course_id,
                 score):
        self.grade_id = grade_id
        self.student_id = student_id
        self.course_id = course_id
        self.score = score

    def __repr__(self):
        return f"<Grade(id={self.grade_id}, score={self.score})>"

class Parent:
    def __init__(self, parent_id):
        self.parent_id = parent_id
        self.students = []  # List[Student]

    def add_student(self, student):
        self.students.append(student)

    def view_grades(self, grade_service, student_id: int):
        return grade_service.get_by_student(student_id)

    def __repr__(self):
        return f"<Parent(id={self.parent_id})>"

class Course:
    def __init__(self, course_id, name, professor_id):
        self.course_id = course_id
        self.name = name
        self.professor_id = professor_id
        self.grades = []  # List[Grade]

    def add_grade(self, grade):
        self.grades.append(grade)

    def calculate_average(self):
        if not self.grades:
            return None
        return sum(g.score for g in self.grades) / len(self.grades)

    def __repr__(self):
        return f"<Course(id={self.course_id}, name={self.name})>"

class Student:
    def __init__(self, user_id, parent_id):
        self.user_id = user_id
        self.parent_id = parent_id
        self.grades = []  # List[Grade]

    def receive_grade(self, grade):
        self.grades.append(grade)

    def __repr__(self):
        return f"<Student(id={self.user_id})>"

class Admin:
    def __init__(self, admin_id):
        self.admin_id = admin_id

    def __repr__(self):
        return f"<Admin(id={self.admin_id})>"

class Professor:
    def __init__(self, professor_id):
        self.professor_id = professor_id
        self.courses = []  # List[Course]

    def grade_student(self, student, course, score: int):
        if course not in self.courses:
            raise ValueError("This professor does not teach the course.")
        grade = Grade(grade_id=None, student_id=student.user_id, course_id=course.course_id, score=score)
        course.add_grade(grade)
        student.receive_grade(grade)
        return grade

    def __repr__(self):
        return f"<Professor(id={self.professor_id})>"
    
class Enrollment:
    def __init__(self, enrollment_id, user_id, course_id):
        self.enrollment_id = enrollment_id
        self.user_id = user_id
        self.course_id = course_id

    def __repr__(self):
        return f"<Enrollment(id={self.enrollment_id}, user_id={self.user_id}, course_id={self.course_id})>"
