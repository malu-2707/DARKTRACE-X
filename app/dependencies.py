from fastapi import Depends

from app.security.authentication import get_current_user


def authenticated_user(
    user: str = Depends(get_current_user),
) -> str:
    return user