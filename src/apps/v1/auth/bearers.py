from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .services import decode_jwt_service


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True) -> None:
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds: HTTPAuthorizationCredentials | None = await super().__call__(request)

        if creds:
            if not creds.scheme == "Bearer":
                raise HTTPException(403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(creds.credentials):
                raise HTTPException(403, detail="Invalid token or expired token")
        else:
            raise HTTPException(403, detail="Invalid authorization code")
        return creds

    @staticmethod
    def verify_jwt(jwt_token: str) -> bool:
        if decode_jwt_service(jwt_token):
            return True
        return False
