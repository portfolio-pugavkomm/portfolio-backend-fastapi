from fastapi import APIRouter, HTTPException

from src.dependencies import DBSessionDep
from src.tags import AUTH_TAG

from .exceptions import UserNameAlreadyUsed
from .schemas import (
    JWTTokenResponseSchema,
    RefreshTokenSchema,
    UserLoginSchema,
    UserRegistrationSchema,
    UserSchema,
)
from .services import (
    CheckUserLoginCredsService,
    refresh_token_service,
    register_user_service,
    sign_jwt_service,
)

router = APIRouter(
    prefix="/auth",
    tags=[AUTH_TAG],
)


@router.post(
    "/register",
    responses={409: {"description": "Username or email already used. Try login."}},
    status_code=201,
)
async def register(data: UserRegistrationSchema, ses: DBSessionDep) -> UserSchema:
    try:
        return await register_user_service(data, ses)
    except UserNameAlreadyUsed:
        raise HTTPException(409)


@router.post("/login_with_pass")
async def login_with_pass(creds: UserLoginSchema, ses: DBSessionDep) -> JWTTokenResponseSchema:
    check_service = CheckUserLoginCredsService(creds, ses)
    if user_id := await check_service.execute():
        return sign_jwt_service(user_id)
    else:
        raise HTTPException(401)


@router.post("/token/refresh")
def refresh_access_token(refresh: RefreshTokenSchema) -> JWTTokenResponseSchema:
    return refresh_token_service(refresh.refresh)
