from app.domain.services.auth_service import AuthService


class AuthController:
    def __init__(self):
        self.service = AuthService()

    def login(self, email: str, password: str) -> dict:
        if not email or not password:
            return {
                "status": "error",
                "message": "Email y contraseña son obligatorios.",
            }

        result = self.service.authenticate(email, password)
        if result.get("status") == "error":
            return {"status": "error", "message": result.get("message")}

        user = result.get("user")
        return {
            "status": "success",
            "user": {
                "user_id": user.user_id,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role,
            },
            "role_display": self.service.get_role_display_name(user.role),
            "permissions": self.service.get_user_permissions(user.role),
        }

    def register(self, full_name: str, email: str, password: str, confirm: str) -> dict:
        if not all([full_name, email, password, confirm]):
            return {"status": "error", "message": "Todos los campos son obligatorios."}

        validation = self.service.validate_registration_data(full_name, email, password, confirm)
        if validation.get("status") == "error":
            return {"status": "error", "message": validation.get("message")}

        result = self.service.register_user(full_name, email, password)
        if result.get("status") == "error":
            return {"status": "error", "message": result.get("message")}

        user = result.get("user")
        return {
            "status": "success",
            "message": "Usuario registrado satisfactoriamente. Su cuenta quedará pendiente de activación.",
            "user": {
                "user_id": user.user_id,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role,
            },
        }

    def logout(self) -> dict:
        return {"status": "success", "message": "Sesión cerrada."}

