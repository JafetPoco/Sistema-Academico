from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.database import db
from datetime import datetime, timezone

class user_dto(db.Model):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    role = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<UserDTO(id={self.user_id}, email={self.email})>"

class announcement_dto(db.Model):
    __tablename__ = 'announcements'

    announcement_id = Column(Integer, primary_key=True)
    course_id       = Column(Integer, ForeignKey('courses.course_id'),  nullable=False)
    user_id         = Column(Integer, ForeignKey('users.user_id'),      nullable=False)
    title           = Column(String(255), nullable=False)
    content         = Column(Text, nullable=False)
    created_at      = Column(DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"<AnnouncementDTO(id={self.announcement_id}, title={self.title})>"

class grade_dto(db.Model):
    __tablename__ = 'grades'

    grade_id    = Column(String(36), primary_key=True)
    student_id  = Column(Integer, ForeignKey('students.user_id'), nullable=False)
    course_id   = Column(Integer, ForeignKey('courses.course_id'), nullable=False)
    score       = Column(Integer, nullable=False)

    student = relationship('student_dto', back_populates='grades')
    course  = relationship('course_dto',  back_populates='grades')

    def __repr__(self):
        return f"<GradeDTO(id={self.grade_id}, score={self.score})>"

class parent_dto(db.Model):
    __tablename__ = 'parents'

    parent_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    students  = relationship('student_dto', back_populates='parent')

    def __repr__(self):
        return f"<ParentDTO(id={self.parent_id})>"

class course_dto(db.Model):
    __tablename__ = 'courses'

    course_id    = Column(Integer, primary_key=True)
    name         = Column(String(100), nullable=False)
    professor_id = Column(Integer, ForeignKey('professors.professor_id'), nullable=False)

    professor = relationship('professor_dto', back_populates='courses')
    grades    = relationship('grade_dto',     back_populates='course')

    def __repr__(self):
        return f"<CourseDTO(id={self.course_id}, name={self.name})>"

class student_dto(db.Model):
    __tablename__ = 'students'

    user_id   = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    parent_id = Column(Integer, ForeignKey('parents.parent_id'), nullable=True)

    parent = relationship('parent_dto', back_populates='students')
    grades = relationship('grade_dto',   back_populates='student')

    def __repr__(self):
        return f"<StudentDTO(id={self.user_id})>"

class admin_dto(db.Model):
    __tablename__ = 'administrators'

    admin_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)

    def __repr__(self):
        return f"<AdminDTO(id={self.admin_id})>"

class professor_dto(db.Model):
    __tablename__ = 'professors'

    professor_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    courses      = relationship('course_dto', back_populates='professor')

    def __repr__(self):
        return f"<ProfessorDTO(id={self.professor_id})>"
