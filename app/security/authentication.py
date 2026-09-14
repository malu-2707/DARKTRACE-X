from fastapi import Header, HTTPException

from app.security.jwt import decode_access_token


def get_current_user(authorization: str | None = Header(default=None)) -> str:
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header required"
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization format"
        )

    token = authorization.split(" ", 1)[1]

    try:
        payload = decode_access_token(token)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    subject = payload.get("sub")

    if not subject:
        raise HTTPException(
            status_code=401,
            detail="Invalid token subject"
        )

    return subject