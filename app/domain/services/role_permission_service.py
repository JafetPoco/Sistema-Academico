"""
Role Permission Service for managing role-based access control.

This service encapsulates all role permission logic, separating it from
authentication concerns and providing a clean interface for authorization checks.
"""
from app.domain.roles import Role, RolePermissions, RoleHierarchy
from typing import List, Set


class RolePermissionService:
    """
    Service responsible for managing role-based permissions and access control.
    
    This service provides methods to check permissions, access rights, and
    other role-related authorization logic, following the Single Responsibility Principle.
    """
    
    def __init__(self):
        """Initialize the role permission service."""
        pass
    
    def get_user_permissions(self, role: int) -> List[str]:
        """
        Get the list of permissions for a given role.
        
        Args:
            role: The role integer value
            
        Returns:
            List of permission strings for the role
        """
        return RolePermissions.get_permissions(role)
    
    def get_role_display_name(self, role: int) -> str:
        """
        Get the human-readable display name for a role.
        
        Args:
            role: The role integer value
            
        Returns:
            Display name of the role in Spanish
        """
        return RolePermissions.get_display_name(role)
    
    def has_permission(self, role: int, permission: str) -> bool:
        """
        Check if a role has a specific permission.
        
        Args:
            role: The role integer value
            permission: The permission to check
            
        Returns:
            True if role has the permission, False otherwise
        """
        return RolePermissions.has_permission(role, permission)
    
    def can_access_qualification(self, role: int) -> bool:
        """
        Check if a role can access the qualification/grading system.
        
        Args:
            role: The role integer value
            
        Returns:
            True if role can assign grades, False otherwise
        """
        return RolePermissions.can_access_qualification(role)
    
    def is_admin(self, role: int) -> bool:
        """
        Check if a role is an administrator.
        
        Args:
            role: The role integer value
            
        Returns:
            True if role is admin, False otherwise
        """
        return RolePermissions.is_admin(role)
    
    def is_teacher(self, role: int) -> bool:
        """
        Check if a role is a teacher.
        
        Args:
            role: The role integer value
            
        Returns:
            True if role is teacher, False otherwise
        """
        return RolePermissions.is_teacher(role)
    
    def is_parent(self, role: int) -> bool:
        """
        Check if a role is a parent.
        
        Args:
            role: The role integer value
            
        Returns:
            True if role is parent, False otherwise
        """
        return RolePermissions.is_parent(role)
    
    def is_teacher_or_admin(self, role: int) -> bool:
        """
        Check if a role is either a teacher or administrator.
        
        Args:
            role: The role integer value
            
        Returns:
            True if role is teacher or admin, False otherwise
        """
        return RolePermissions.is_teacher_or_admin(role)
    
    def can_view_grades(self, role: int) -> bool:
        """
        Check if a role can view grades.
        
        Args:
            role: The role integer value
            
        Returns:
            True if role can view grades, False otherwise
        """
        role_enum = Role.from_int(role)
        return role_enum in RoleHierarchy.CAN_VIEW_GRADES
    
    def can_assign_grades(self, role: int) -> bool:
        """
        Check if a role can assign/modify grades.
        
        Args:
            role: The role integer value
            
        Returns:
            True if role can assign grades, False otherwise
        """
        role_enum = Role.from_int(role)
        return role_enum in RoleHierarchy.CAN_ASSIGN_GRADES
    
    def can_manage_users(self, role: int) -> bool:
        """
        Check if a role can manage users.
        
        Args:
            role: The role integer value
            
        Returns:
            True if role can manage users, False otherwise
        """
        role_enum = Role.from_int(role)
        return role_enum in RoleHierarchy.CAN_MANAGE_USERS
    
    def can_manage_courses(self, role: int) -> bool:
        """
        Check if a role can manage courses.
        
        Args:
            role: The role integer value
            
        Returns:
            True if role can manage courses, False otherwise
        """
        role_enum = Role.from_int(role)
        return role_enum in RoleHierarchy.CAN_MANAGE_COURSES
    
    def can_manage_announcements(self, role: int) -> bool:
        """
        Check if a role can manage announcements.
        
        Args:
            role: The role integer value
            
        Returns:
            True if role can manage announcements, False otherwise
        """
        role_enum = Role.from_int(role)
        return role_enum in RoleHierarchy.CAN_MANAGE_ANNOUNCEMENTS
