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
import logging
from sqlalchemy.exc import SQLAlchemyError

class BaseRepository:
    dto = None
    mapper = None

    def add(self, domain_obj):
        dto_obj = self.mapper.to_dto(domain_obj)
        try:
            db.session.add(dto_obj)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding {self.dto.__tablename__}: {e}")
            return False, str(e)

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

class AnnouncementRepository(BaseRepository):
    dto = AnnouncementDTO
    mapper = AnnouncementMapper

class GradeRepository(BaseRepository):
    dto = GradeDTO
    mapper = GradeMapper

class ParentRepository(BaseRepository):
    dto = ParentDTO
    mapper = ParentMapper

class CourseRepository(BaseRepository):
    dto = CourseDTO
    mapper = CourseMapper

class StudentRepository(BaseRepository):
    dto = StudentDTO
    mapper = StudentMapper

class AdminRepository(BaseRepository):
    dto = AdminDTO
    mapper = AdminMapper

class ProfessorRepository(BaseRepository):
    dto = ProfessorDTO
    mapper = ProfessorMapper
