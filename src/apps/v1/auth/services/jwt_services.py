import time
from typing import Any
from uuid import UUID

import jwt
from fastapi import HTTPException

from ..config import get_config
from ..schemas import JWTTokenResponseSchema

settings = get_config()


def sign_jwt_service(user_id: UUID | str, rotate_refresh: bool = True) -> JWTTokenResponseSchema:
    payload = {
        "user_id": str(user_id),
        "type": "access",
        "expires": time.time() + settings.JWT_ACCESS_EXPIRES,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    refresh: None | str = None

    if rotate_refresh:
        payload_refresh = {
            "user_id": str(user_id),
            "type": "refresh",
            "expires": time.time() + settings.JWT_REFRESH_EXPIRES,
        }
        refresh = jwt.encode(payload_refresh, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    return JWTTokenResponseSchema(access=token, refresh=refresh)


def refresh_token_service(refresh_token: str) -> JWTTokenResponseSchema:
    if payload := decode_jwt_service(refresh_token):
        if payload.get("type") != "refresh":
            raise HTTPException(401, detail="Wrong token type")
        return sign_jwt_service(payload.get("user_id"), settings.ROTATE_REFRESH)  # type: ignore
    raise HTTPException(401, "Wrong token or expired")


def decode_jwt_service(jwt_token: str) -> dict[str, Any] | None:
    try:
        decoded_token = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=(settings.JWT_ALGORITHM,))
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except Exception as e:
        # TODO: logging
        print(e)
        return None
