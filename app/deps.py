import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import get_settings

bearer_scheme = HTTPBearer(auto_error=False)


def verify_api_key(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> None:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    settings = get_settings()
    allowed = settings.api_keys_set
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="API key authentication is not configured",
        )
    token = credentials.credentials
    for key in allowed:
        if secrets.compare_digest(token, key):
            return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API key",
    )
