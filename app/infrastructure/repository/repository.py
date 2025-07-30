# infrastructure/repository/repository.py
from app.infrastructure.database import db
from app.infrastructure.repository.models import (
    UserDTO,
    AnnouncementDTO,
    GradeDTO,
    ParentDTO,
    CourseDTO,
    StudentDTO,
    AdminDTO,
    ProfessorDTO,
    EnrollmentDTO
)
from app.infrastructure.repository.mapper import (
    UserMapper,
    AnnouncementMapper,
    GradeMapper,
    ParentMapper,
    CourseMapper,
    StudentMapper,
    AdminMapper,
    ProfessorMapper,
    EnrollmentMapper
)

from app.domain.entities import User, Announcement, Grade, Parent, Course, Student, Admin, Professor, Enrollment
import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
from typing import List

class BaseRepository:
    dto = None
    mapper = None

    def add(self, domain_obj):
        dto_obj = self.mapper.to_dto(domain_obj)
        try:
            db.session.add(dto_obj)
            db.session.commit()
            return self.mapper.to_domain(dto_obj), None  # devuelves el user con ID seteado
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding {self.dto.__tablename__}: {e}")
            return None, str(e)


    def remove(self, obj_id):
        try:
            dto_obj = self.dto.query.get(obj_id)
            if not dto_obj:
                return False
            db.session.delete(dto_obj)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error removing {self.dto.__tablename__}: {e}")
            return False

    def update(self, obj_id, data: dict):
        try:
            dto_obj = self.dto.query.get(obj_id)
            if not dto_obj:
                return False
            for key, value in data.items():
                setattr(dto_obj, key, value)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating {self.dto.__tablename__}: {e}")
            return False

    def get(self, obj_id):
        try:
            dto_obj = self.dto.query.get(obj_id)
            return self.mapper.to_domain(dto_obj) if dto_obj else None
        except Exception as e:
            logging.error(f"Error fetching {self.dto.__tablename__}: {e}")
            return None

    def list_all(self):
        try:
            dto_objs = self.dto.query.all()
            return [self.mapper.to_domain(dto) for dto in dto_objs]
        except SQLAlchemyError as e:
            logging.error(f"Database error listing {self.dto.__tablename__}: {e}")
            return []
        except Exception as e:
            logging.error(f"Unexpected error listing {self.dto.__tablename__}: {e}")
            return []

# Repositories for each model
class UserRepository(BaseRepository):
    dto = UserDTO
    mapper = UserMapper

    def find_by_email(self, email: str):
        try:
            user_dto = self.dto.query.filter_by(email=email).first()
            return self.mapper.to_domain(user_dto) if user_dto else None
        except Exception as e:
            logging.error(f"Error finding user by email: {e}")
            return None

    def create(self, user: User):
        return self.add(user)
    
    def list_by_role(self, role: int):
        try:
            dtos = self.dto.query.filter_by(role=role).all()
            return [self.mapper.to_domain(d) for d in dtos]
        except Exception as e:
            logging.error(f"Error listing users by role {role}: {e}")
            return []


class AnnouncementRepository(BaseRepository):
    dto = AnnouncementDTO
    mapper = AnnouncementMapper

    def find_public(self) -> List[Announcement]:
        dtos = self.dto.query.filter_by(is_private=False).all()
        return [self.mapper.to_domain(d) for d in dtos]

    def find_private(self) -> List[Announcement]:
        dtos = self.dto.query.filter_by(is_private=True).all()
        return [self.mapper.to_domain(d) for d in dtos]

    def find_private_for_user(self, user_id: int) -> List[Announcement]:
        dtos = (
            self.dto.query
                .filter(self.dto.is_private.is_(True))
                .filter_by(user_id=user_id)
                .all()
        )
        return [self.mapper.to_domain(d) for d in dtos]

class GradeRepository(BaseRepository):
    dto = GradeDTO
    mapper = GradeMapper

    def get_scores_with_student_names_by_course(self, course_id: int):
        query = (
            db.session.query(
                GradeDTO.score,
                StudentDTO.user_id,
                UserDTO.full_name
            )
            .join(StudentDTO, GradeDTO.student_id == StudentDTO.user_id)
            .join(UserDTO, StudentDTO.user_id == UserDTO.user_id)
            .filter(GradeDTO.course_id == course_id)
        )

        return query.all()
    
    def get_by_student_id(self, student_id):
        try:
            grades_dto = self.dto.query.filter_by(student_id=student_id).all()
            return [self.mapper.to_domain(dto) for dto in grades_dto]
        except Exception as e:
            logging.error(f"Error fetching grades by student_id: {e}")
            return []
        
    def get_grades_by_student(self, student_id: int):
        try:
            grades_dto = self.dto.query.filter_by(student_id=student_id).all()
            grades = []
            for dto in grades_dto:
                try:
                    grade = self.mapper.to_domain(dto)
                    grades.append(grade)
                except Exception as e:
                    grades.append({
                        'score': dto.score,
                        'student_id': dto.student_id,
                        'course_id': dto.course_id
                    })

            return grades, None

        except Exception as e:
            return [], f"Error: {str(e)}"
        
    def get_average_by_course_id(self, course_id: int):
        try:
            scores = (
                db.session.query(GradeDTO.score)
                .filter(GradeDTO.course_id == course_id)
                .all()
            )

            score_list = [score for (score,) in scores]

            if not score_list:
                return 0.0

            average = sum(score_list) / len(score_list)
            return round(average, 2)
        except Exception as e:
            logging.error(f"Error al calcular promedio sin func para curso {course_id}: {e}")
            return 0.0


        
class ParentRepository(BaseRepository):
    dto = ParentDTO
    mapper = ParentMapper

    def get_children_by_parent(self, parent_id: int):
        try:
            children_query = db.session.query(
                UserDTO.user_id,
                UserDTO.full_name,
                UserDTO.email
            ).join(
                StudentDTO, StudentDTO.user_id == UserDTO.user_id
            ).filter(
                StudentDTO.parent_id == parent_id,
                UserDTO.role == 0
            ).all()
            
            children = []
            for row in children_query:
                children.append({
                    'id': row.user_id,
                    'name': row.full_name,
                    'email': row.email,
                    'relationship': 'Hijo/a'
                })
            return children, None

        except Exception as e:
            return [], f"Error: {str(e)}"

class CourseRepository(BaseRepository):
    dto = CourseDTO
    mapper = CourseMapper

    def get_courses_by_professor(self, professor_id):
        try:
            result = db.session.query(
                CourseDTO.course_id,
                CourseDTO.name,
                CourseDTO.professor_id
            ).filter(
                CourseDTO.professor_id == professor_id
            ).all()
            
            courses_data = []
            for row in result:
                course_info = {
                    'id': row.course_id,
                    'name': row.name,
                    'professor_id': row.professor_id
                }
                courses_data.append(course_info)
            
            return courses_data, None
            
        except Exception as e:
            logging.error(f"Error getting courses for professor {professor_id}: {e}")
            return [], f"Error: {str(e)}"
    
    def get_all_courses(self):
        try:
            result = db.session.query(
                CourseDTO.course_id,
                CourseDTO.name,
                CourseDTO.professor_id
            ).all()
            
            courses_data = []
            for row in result:
                course_info = {
                    'id': row.course_id,
                    'name': row.name,
                    'professor_id': row.professor_id
                }
                courses_data.append(course_info)
            
            return courses_data, None
            
        except Exception as e:
            return [], f"Error: {str(e)}"
        
    def get_course_name_by_id(self, course_id):
        course = CourseDTO.query.get(course_id)
        return course.name if course else None


class StudentRepository(BaseRepository):
    dto = StudentDTO
    mapper = StudentMapper
    def get_by_parent_id(self, parent_id):
        try:
            students_dto = self.dto.query.filter_by(parent_id=parent_id).all()
            return [self.mapper.to_domain(dto) for dto in students_dto]
        except Exception as e:
            logging.error(f"Error fetching students by parent_id: {e}")
            return []
    def get_students_with_names(self):
        try:
            # Query con INNER JOIN
            result = db.session.query(
                UserDTO.full_name,    # u.full_name
                UserDTO.user_id       # u.user_id
            ).select_from(StudentDTO).join(   # FROM students s INNER JOIN users u
                UserDTO, StudentDTO.user_id == UserDTO.user_id
            ).all()
            
            # Convertir resultado a lista de diccionarios
            students_data = []
            for row in result:
                student_info = {
                    'id': row.user_id,
                    'name': row.full_name
                }
                students_data.append(student_info)
            
            return students_data, None  # (result, error)
            
        except SQLAlchemyError as e:
            logging.error(f"Database error getting students with names: {e}")
            return [], f"Error de base de datos: {str(e)}"
        except Exception as e:
            logging.error(f"Unexpected error getting students with names: {e}")
            return [], f"Error inesperado: {str(e)}"

class AdminRepository(BaseRepository):
    dto = AdminDTO
    mapper = AdminMapper

class ProfessorRepository(BaseRepository):
    dto = ProfessorDTO
    mapper = ProfessorMapper

class EnrollmentRepository(BaseRepository):
    dto = EnrollmentDTO
    mapper = EnrollmentMapper

    def get_by_user_id(self, user_id: int):
        """Obtener todas las matrículas de un usuario"""
        try:
            enrollments_dto = self.dto.query.filter_by(user_id=user_id).all()
            return [self.mapper.to_domain(dto) for dto in enrollments_dto]
        except Exception as e:
            logging.error(f"Error fetching enrollments by user_id: {e}")
            return []

    def get_by_course_id(self, course_id: int):
        """Obtener todas las matrículas de un curso"""
        try:
            enrollments_dto = self.dto.query.filter_by(course_id=course_id).all()
            return [self.mapper.to_domain(dto) for dto in enrollments_dto]
        except Exception as e:
            logging.error(f"Error fetching enrollments by course_id: {e}")
            return []

    def get_user_courses_with_names(self, user_id: int):
        """Obtener cursos de un usuario con nombres"""
        try:
            result = db.session.query(
                CourseDTO.course_id,
                CourseDTO.name
            ).select_from(EnrollmentDTO).join(
                CourseDTO, EnrollmentDTO.course_id == CourseDTO.course_id
            ).filter(
                EnrollmentDTO.user_id == user_id
            ).all()
            
            courses_data = []
            for row in result:
                course_info = {
                    'id': row.course_id,
                    'name': row.name
                }
                courses_data.append(course_info)
            
            return courses_data, None
            
        except Exception as e:
            logging.error(f"Error getting user courses with names: {e}")
            return [], f"Error: {str(e)}"

    def get_course_students_with_names(self, course_id: int):
        """Obtener estudiantes de un curso con nombres"""
        try:
            result = db.session.query(
                UserDTO.user_id,
                UserDTO.full_name
            ).select_from(EnrollmentDTO).join(
                UserDTO, EnrollmentDTO.user_id == UserDTO.user_id
            ).filter(
                EnrollmentDTO.course_id == course_id
            ).all()
            
            students_data = []
            for row in result:
                student_info = {
                    'id': row.user_id,
                    'name': row.full_name
                }
                students_data.append(student_info)
            
            return students_data, None
            
        except Exception as e:
            logging.error(f"Error getting course students with names: {e}")
            return [], f"Error: {str(e)}"

    def is_user_enrolled(self, user_id: int, course_id: int):
        """Verificar si un usuario está matriculado en un curso"""
        try:
            enrollment = self.dto.query.filter_by(
                user_id=user_id,
                course_id=course_id
            ).first()
            return enrollment is not None
        except Exception as e:
            logging.error(f"Error checking enrollment: {e}")
            return False

    def enroll_user(self, user_id: int, course_id: int):
        """Matricular un usuario en un curso"""
        try:
            # Verificar si ya existe
            if self.is_user_enrolled(user_id, course_id):
                return None, "El usuario ya está matriculado en este curso"
            
            # Crear nueva matrícula
            enrollment = Enrollment(
                enrollment_id=None,
                user_id=user_id,
                course_id=course_id
            )
            
            return self.add(enrollment)
            
        except Exception as e:
            logging.error(f"Error enrolling user: {e}")
            return None, f"Error: {str(e)}"
        
    def count_students_by_course(self, course_id: int):
        """Contar cuántos estudiantes están matriculados en un curso"""
        try:
            count_students = db.session.query(EnrollmentDTO).filter_by(course_id=course_id).count()
            return count_students
        except Exception as e:
            logging.error(f"Error counting students in course {course_id}: {e}")
            return 0
