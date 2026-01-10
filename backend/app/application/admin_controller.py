from app.domain.services.admin_service import AdminService


class AdminController:
    def __init__(self):
        self.service = AdminService()

    @staticmethod
    def _serialize_user(user):
        if not user:
            return {}
        return {
            "id": user.user_id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role,
        }

    @staticmethod
    def _serialize_course(course):
        if not course:
            return {}
        return {
            "id": course.course_id,
            "name": course.name,
            "professor_id": course.professor_id,
        }

    def handle_update_user(self, user_id: int, role) -> dict:
        try:
            parsed_role = int(role)
        except (TypeError, ValueError):
            return {"success": False, "message": "Rol inválido."}

        updated = self.service.update_user(user_id, parsed_role)
        return {
            "success": updated,
            "message": "Usuario actualizado correctamente." if updated else "Error al actualizar el usuario.",
        }

    def handle_get_users(self) -> dict:
        users = self.service.get_users() or []
        serialized = [self._serialize_user(user) for user in users]
        return {"data": serialized, "count": len(serialized)}

    def handle_create_course(self, course_data: dict) -> dict:
        course, err = self.service.create_course(course_data)
        if err:
            return {"success": False, "message": f"Error al crear el curso. {err}"}
        return {
            "success": True,
            "message": "Curso creado correctamente.",
            "course": self._serialize_course(course),
        }

    def handle_get_courses(self) -> dict:
        courses = self.service.get_courses() or []
        serialized = [self._serialize_course(course) for course in courses]
        return {"data": serialized, "count": len(serialized)}

    def handle_get_professors(self) -> dict:
        professors = self.service.get_professors() or []
        serialized = [self._serialize_user(prof) for prof in professors]
        return {"data": serialized, "count": len(serialized)}
