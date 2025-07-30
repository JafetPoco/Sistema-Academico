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
    ProfessorDTO
)
from app.infrastructure.repository.mapper import (
    UserMapper,
    AnnouncementMapper,
    GradeMapper,
    ParentMapper,
    CourseMapper,
    StudentMapper,
    AdminMapper,
    ProfessorMapper
)

from app.domain.entities import User, Announcement, Grade, Parent, Course, Student, Admin, Professor
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
    def get_by_id(self, id: int):
        try:
            user_dto = self.dto.query.filter_by(user_id=id).first()
            return self.mapper.to_domain(user_dto) if user_dto else None
        except Exception as e:
            logging.error(f"Error finding user by id: {e}")
            return None


    def create(self, user: User):
        return self.add(user)


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
    def get_by_student_id(self, student_id):
        try:
            grades_dto = self.dto.query.filter_by(student_id=student_id).all()
            return [self.mapper.to_domain(dto) for dto in grades_dto]
        except Exception as e:
            logging.error(f"Error fetching grades by student_id: {e}")
            return []
class ParentRepository(BaseRepository):
    dto = ParentDTO
    mapper = ParentMapper

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
        
    def get_names_by_ids(self, course_ids):

        # Asegurarnos de que siempre tengamos una lista
        if isinstance(course_ids, int):
            course_ids = [course_ids]
        if not course_ids:
            return {}

        try:
            # Filtrar usando el nombre real de la columna PK en tu DTO:
            # aquí suponemos `course_id` es la columna primaria
            cursos = (
                self.dto.query
                    .filter(self.dto.course_id.in_(course_ids))
                    .all()
            )
            # Suponemos que el campo de nombre en la tabla es `course_name`
            return { c.course_id: c.name for c in cursos }

        except SQLAlchemyError as e:
            logging.error(f"Error fetching course names for ids {course_ids}: {e}")
            return {}
            
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
