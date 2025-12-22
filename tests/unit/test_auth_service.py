import pytest
from unittest.mock import Mock, patch
from werkzeug.security import generate_password_hash
from app.domain.services.auth_service import AuthService
from app.domain.services.role_permission_service import RolePermissionService
from app.domain.entities import User
from app.domain.roles import Role

@pytest.fixture
def auth_service():
    return AuthService()

@pytest.fixture
def role_permission_service():
    return RolePermissionService()

@pytest.fixture
def mock_user_repo():
    with patch('app.domain.services.auth_service.UserRepository') as mock:
        yield mock.return_value

@pytest.fixture
def sample_user():
    return User(
        user_id=1,
        full_name="Test User",
        email="test@example.com",
        password_hash=generate_password_hash("password123"),
        role=Role.TEACHER
    )

class TestAuthService:
    # Registration Tests
    def test_register_user_success(self, auth_service, mock_user_repo):
        mock_user_repo.find_by_email.return_value = None
        mock_user_repo.create.return_value = (User(1, "Test User", "test@example.com", "hash", 1), None)
        
        result = auth_service.register_user("Test User", "test@example.com", "password123")
        
        assert result["status"] == "success"
        assert result["user"] is not None

    def test_register_user_email_taken(self, auth_service, mock_user_repo):
        mock_user_repo.find_by_email.return_value = User(1, "Existing", "test@example.com", "hash", 1)
        
        result = auth_service.register_user("Test User", "test@example.com", "password123")
        
        assert result["status"] == "error"
        assert "Ya existe" in result["message"]

    def test_register_user_db_error(self, auth_service, mock_user_repo):
        mock_user_repo.find_by_email.return_value = None
        mock_user_repo.create.return_value = (None, "Database error")
        
        result = auth_service.register_user("Test User", "test@example.com", "password123")
        
        assert result["status"] == "error"
        assert result["message"] == "Database error"

    # Authentication Tests
    def test_authenticate_success(self, auth_service, mock_user_repo, sample_user):
        mock_user_repo.find_by_email.return_value = sample_user
        
        result = auth_service.authenticate("test@example.com", "password123")
        
        assert result["status"] == "success"
        assert result["user"] == sample_user

    def test_authenticate_user_not_found(self, auth_service, mock_user_repo):
        mock_user_repo.find_by_email.return_value = None
        
        result = auth_service.authenticate("nonexistent@example.com", "password123")
        
        assert result["status"] == "error"
        assert "no registrado" in result["message"]

    def test_authenticate_inactive_user(self, auth_service, mock_user_repo):
        inactive_user = User(1, "Inactive", "inactive@example.com", "hash", Role.UNKNOWN)
        mock_user_repo.find_by_email.return_value = inactive_user
        
        result = auth_service.authenticate("inactive@example.com", "password123")
        
        assert result["status"] == "error"
        assert "no se activo" in result["message"]

    def test_authenticate_wrong_password(self, auth_service, mock_user_repo, sample_user):
        mock_user_repo.find_by_email.return_value = sample_user
        
        result = auth_service.authenticate("test@example.com", "wrongpassword")
        
        assert result["status"] == "error"
        assert "incorrecta" in result["message"]

    # Validation Tests
    def test_validate_registration_data_success(self, auth_service):
        result = auth_service.validate_registration_data(
            "Test User", "test@example.com", "password123", "password123"
        )
        assert result["status"] == "success"

    def test_validate_registration_data_missing_fields(self, auth_service):
        result = auth_service.validate_registration_data(
            "", "test@example.com", "password123", "password123"
        )
        assert result["status"] == "error"
        assert "obligatorios" in result["message"]

    def test_validate_registration_data_password_mismatch(self, auth_service):
        result = auth_service.validate_registration_data(
            "Test User", "test@example.com", "password123", "different"
        )
        assert result["status"] == "error"
        assert "no coinciden" in result["message"]

    # Role and Permission Tests
    @pytest.mark.parametrize("role,expected", [
        (Role.UNKNOWN, "Unknown"),
        (Role.TEACHER, "Profesor"),
        (Role.ADMIN, "Administrador"),
        (Role.PARENT, "Padre"),
        (99, "Usuario"),  # Invalid role
    ])
    def test_get_role_display_name(self, auth_service, role, expected):
        assert auth_service.get_role_display_name(role) == expected

    @pytest.mark.parametrize("role,expected", [
        (Role.TEACHER, True),
        (Role.ADMIN, False),
        (Role.PARENT, False),
        (Role.UNKNOWN, False),
    ])
    def test_can_access_qualification(self, auth_service, role, expected):
        assert auth_service.can_access_qualification(role) == expected

    @pytest.mark.parametrize("role,expected", [
        (Role.ADMIN, True),
        (Role.TEACHER, False),
        (Role.PARENT, False),
        (Role.UNKNOWN, False),
    ])
    def test_is_admin(self, auth_service, role, expected):
        assert auth_service.is_admin(role) == expected

    @pytest.mark.parametrize("role,expected_permissions", [
        (Role.UNKNOWN, ["view_grades", "view_profile"]),
        (Role.TEACHER, ["qualify_students", "view_courses", "view_reports", "manage_grades"]),
        (Role.PARENT, ["view_children", "view_messages", "view_grades"]),
        (Role.ADMIN, ["manage_users", "manage_courses", "view_all_reports", "manage_system"]),
        (99, []),  # Invalid role should return empty list
    ])
    def test_get_user_permissions(self, auth_service, role, expected_permissions):
        assert auth_service.get_user_permissions(role) == expected_permissions


class TestRolePermissionService:
    """Tests for the RolePermissionService."""
    
    @pytest.mark.parametrize("role,expected", [
        (Role.UNKNOWN, "Unknown"),
        (Role.TEACHER, "Profesor"),
        (Role.ADMIN, "Administrador"),
        (Role.PARENT, "Padre"),
    ])
    def test_get_role_display_name(self, role_permission_service, role, expected):
        assert role_permission_service.get_role_display_name(role) == expected

    def test_is_teacher(self, role_permission_service):
        assert role_permission_service.is_teacher(Role.TEACHER) is True
        assert role_permission_service.is_teacher(Role.ADMIN) is False

    def test_is_admin(self, role_permission_service):
        assert role_permission_service.is_admin(Role.ADMIN) is True
        assert role_permission_service.is_admin(Role.TEACHER) is False

    def test_is_parent(self, role_permission_service):
        assert role_permission_service.is_parent(Role.PARENT) is True
        assert role_permission_service.is_parent(Role.ADMIN) is False

    def test_is_teacher_or_admin(self, role_permission_service):
        assert role_permission_service.is_teacher_or_admin(Role.TEACHER) is True
        assert role_permission_service.is_teacher_or_admin(Role.ADMIN) is True
        assert role_permission_service.is_teacher_or_admin(Role.PARENT) is False

    def test_can_view_grades(self, role_permission_service):
        assert role_permission_service.can_view_grades(Role.PARENT) is True
        assert role_permission_service.can_view_grades(Role.TEACHER) is True
        assert role_permission_service.can_view_grades(Role.ADMIN) is True
        assert role_permission_service.can_view_grades(Role.UNKNOWN) is False

    def test_can_assign_grades(self, role_permission_service):
        assert role_permission_service.can_assign_grades(Role.TEACHER) is True
        assert role_permission_service.can_assign_grades(Role.ADMIN) is True
        assert role_permission_service.can_assign_grades(Role.PARENT) is False

    def test_can_manage_users(self, role_permission_service):
        assert role_permission_service.can_manage_users(Role.ADMIN) is True
        assert role_permission_service.can_manage_users(Role.TEACHER) is False

    def test_can_manage_courses(self, role_permission_service):
        assert role_permission_service.can_manage_courses(Role.TEACHER) is True
        assert role_permission_service.can_manage_courses(Role.ADMIN) is True
        assert role_permission_service.can_manage_courses(Role.PARENT) is False
