from enum import StrEnum
from app.models.membership import Role
class Permission(StrEnum):
    ORG_UPDATE="org:update"; MEMBER_MANAGE="member:manage"; WORKSPACE_CREATE="workspace:create"; PROJECT_CREATE="project:create"; PROJECT_READ="project:read"; PROJECT_UPDATE="project:update"; PROJECT_DELETE="project:delete"
ROLE_PERMISSIONS={
 Role.OWNER:set(Permission),
 Role.ADMIN:{Permission.ORG_UPDATE,Permission.MEMBER_MANAGE,Permission.WORKSPACE_CREATE,Permission.PROJECT_CREATE,Permission.PROJECT_READ,Permission.PROJECT_UPDATE,Permission.PROJECT_DELETE},
 Role.DEVELOPER:{Permission.WORKSPACE_CREATE,Permission.PROJECT_CREATE,Permission.PROJECT_READ,Permission.PROJECT_UPDATE,Permission.PROJECT_DELETE},
 Role.VIEWER:{Permission.PROJECT_READ},
}
def has_permission(role:Role,permission:Permission)->bool: return permission in ROLE_PERMISSIONS[role]
