from werkzeug.security import check_password_hash
from app.infrastructure.repository.repository import UserRepository
from app.domain.entities import User
from app.domain.factories.user_factory import UserFactory
from app.domain.roles import Role
from app.domain.services.role_permission_service import RolePermissionService

class AuthService:
    """
    Authentication service for user login and registration.
    
    Handles authentication logic and delegates role/permission checks
    to RolePermissionService following Single Responsibility Principle.
    """
    
    # Deprecated: Use app.domain.roles.Role enum instead
    UNKNOWN_ROLE = Role.UNKNOWN
    TEACHER_ROLE = Role.TEACHER
    ADMIN_ROLE = Role.ADMIN
    PARENT_ROLE = Role.PARENT

    def __init__(self, user_repo: UserRepository | None = None, 
                 user_factory: type[UserFactory] = UserFactory,
                 role_permission_service: RolePermissionService | None = None):
        self.user_repo = user_repo or UserRepository()
        self.user_factory = user_factory
        self.role_permission_service = role_permission_service or RolePermissionService()

    def is_email_taken(self, email):
        return self.user_repo.find_by_email(email) is not None

    def register_user(self, full_name: str, email: str, password: str, role: int = 0):
        if self.is_email_taken(email):
            return {"status": "error", "message": "Ya existe un usuario con este correo"}

        new_user = self.user_factory.create_with_raw_password(full_name, email, password, role)

        created_user, err = self.user_repo.create(new_user)
        if err:
            return {"status": "error", "message": err}

        return {"status": "success", "user": created_user}
    
    def authenticate(self, email: str, password: str) -> dict:
        user = self.user_repo.find_by_email(email)
        if not user:
            return {"status": "error", "message": "Usuario no registrado"}

        if user.role == Role.UNKNOWN:
            return {"status": "error", "message": "Aun no se activo su cuenta, contáctese con un administrador si cree que esto se trata de un error."}

        if not check_password_hash(user.password_hash, password):
            return {"status": "error", "message": "Contraseña incorrecta"}

        return {"status": "success", "user": user}

    def validate_registration_data(self, full_name, email, password, confirm):
        if not full_name or not email or not password or not confirm:
            return {"status": "error", "message": "Todos los campos son obligatorios."}
        
        if password != confirm:
            return {"status": "error", "message": "Las contraseñas no coinciden."}
        
        return {"status": "success"}

    def get_role_display_name(self, role: int) -> str:
        """Get display name for a role. Delegates to RolePermissionService."""
        return self.role_permission_service.get_role_display_name(role)
    
    def can_access_qualification(self, role: int) -> bool:
        """Check if role can access qualification system. Delegates to RolePermissionService."""
        return self.role_permission_service.can_access_qualification(role)
    
    def is_admin(self, role: int) -> bool:
        """Check if role is admin. Delegates to RolePermissionService."""
        return self.role_permission_service.is_admin(role)
    
    def get_user_permissions(self, role: int) -> list:
        """Get permissions for a role. Delegates to RolePermissionService."""
        return self.role_permission_service.get_user_permissions(role)
