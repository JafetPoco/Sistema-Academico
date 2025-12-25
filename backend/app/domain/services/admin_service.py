from app.infrastructure.repository.repository import UserRepository
from app.infrastructure.repository.repository import CourseRepository
from app.domain.entities import User, Course

class AdminService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.course_repository = CourseRepository()

    def update_user(self, user_id: int, role: int):
        user = self.user_repository.get(user_id)
        if user:
            user.role = role
            self.user_repository.update(user.user_id, {'role': role})
            return True
        return False
    
    def get_users(self):
        return self.user_repository.list_all()
    
    def create_course(self, course_data):
        course = Course(
            course_id=None,
            name=course_data['name'],
            professor_id=course_data['professor_id']
        )
        return self.course_repository.add(course)

    def get_courses(self):
        return self.course_repository.list_all()

    def get_professors(self):
        return self.user_repository.list_by_role(role=1)