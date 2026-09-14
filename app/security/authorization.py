from fastapi import HTTPException


ROLE_PERMISSIONS = {
    "analyst": {
        "view_alerts",
        "view_investigations",
        "approve_response",
        "view_audit",
    },
    "admin": {
        "view_alerts",
        "view_investigations",
        "approve_response",
        "view_audit",
        "manage_users",
        "manage_policies",
    },
}


def check_permission(role: str, permission: str) -> bool:
    permissions = ROLE_PERMISSIONS.get(role, set())

    if permission not in permissions:
        raise HTTPException(
            status_code=403,
            detail="Permission denied"
        )

    return True