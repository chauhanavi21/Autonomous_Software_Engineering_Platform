from app.auth.permissions import Permission,has_permission
from app.models.membership import Role
def test_viewer_can_read_but_not_create(): assert has_permission(Role.VIEWER,Permission.PROJECT_READ); assert not has_permission(Role.VIEWER,Permission.PROJECT_CREATE)
def test_owner_has_all_permissions(): assert all(has_permission(Role.OWNER,p) for p in Permission)
