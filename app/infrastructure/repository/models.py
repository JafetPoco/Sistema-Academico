from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.infrastructure.database import db
from datetime import datetime, timezone

class UserDTO(db.Model):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    role = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<UserDTO(id={self.user_id}, email={self.email})>"

class AnnouncementDTO(db.Model):
    __tablename__ = 'announcements'

    announcement_id = Column(Integer, primary_key=True)
    course_id       = Column(Integer, ForeignKey('courses.course_id'),  nullable=True)
    user_id         = Column(Integer, ForeignKey('users.user_id'),      nullable=True)
    title           = Column(String(255), nullable=False)
    content         = Column(Text, nullable=False)
    is_private      = Column(Boolean, default=False)
    created_at      = Column(DateTime, default=datetime.now(timezone.utc))

    course = relationship('CourseDTO', back_populates='announcements')

    def __repr__(self):
        return f"<AnnouncementDTO(id={self.announcement_id}, title={self.title})>"

class GradeDTO(db.Model):
    __tablename__ = 'grades'

    grade_id    = Column(String(36), primary_key=True)
    student_id  = Column(Integer, ForeignKey('students.user_id'), nullable=False)
    course_id   = Column(Integer, ForeignKey('courses.course_id'), nullable=False)
    score       = Column(Integer, nullable=False)

    student = relationship('StudentDTO', back_populates='grades')
    course  = relationship('CourseDTO',  back_populates='grades')

    def __repr__(self):
        return f"<GradeDTO(id={self.grade_id}, score={self.score})>"

class ParentDTO(db.Model):
    __tablename__ = 'parents'

    parent_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    students  = relationship('StudentDTO', back_populates='parent')

    def __repr__(self):
        return f"<ParentDTO(id={self.parent_id})>"

class CourseDTO(db.Model):
    __tablename__ = 'courses'

    course_id    = Column(Integer, primary_key=True)
    name         = Column(String(100), nullable=False)
    professor_id = Column(Integer, ForeignKey('professors.professor_id'), nullable=False)

    professor = relationship('ProfessorDTO', back_populates='courses')
    grades    = relationship('GradeDTO',     back_populates='course')
    announcements = relationship('AnnouncementDTO', back_populates='course')

    def __repr__(self):
        return f"<CourseDTO(id={self.course_id}, name={self.name})>"

class StudentDTO(db.Model):
    __tablename__ = 'students'

    user_id   = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    parent_id = Column(Integer, ForeignKey('parents.parent_id'), nullable=True)

    parent = relationship('ParentDTO', back_populates='students')
    grades = relationship('GradeDTO',   back_populates='student')

    def __repr__(self):
        return f"<StudentDTO(id={self.user_id})>"

class AdminDTO(db.Model):
    __tablename__ = 'administrators'

    admin_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)

    def __repr__(self):
        return f"<AdminDTO(id={self.admin_id})>"

class ProfessorDTO(db.Model):
    __tablename__ = 'professors'

    professor_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    courses      = relationship('CourseDTO', back_populates='professor')

    def __repr__(self):
        return f"<ProfessorDTO(id={self.professor_id})>"
