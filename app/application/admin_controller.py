from app.domain.services.admin_service import AdminService

class AdminController:
    def __init__(self):
        self.service = AdminService()

    def handle_update_user(self, user_id: int, role: int):
        if self.service.update_user(user_id, role):
            return "success", "Usuario actualizado correctamente."
        return "danger", "Error al actualizar el usuario."

    def handle_get_users(self):
        users = self.service.get_users()
        return users
    
    def handle_create_course(self, course_data):
        _, err = self.service.create_course(course_data)
        if err:
            return "danger", f"Error al crear el curso. {err}"
        return "success", "Curso creado correctamente."

    def handle_get_courses(self):
        courses = self.service.get_courses()
        return courses
    
    def handle_get_professors(self):
        professors = self.service.get_professors()
        return professors
