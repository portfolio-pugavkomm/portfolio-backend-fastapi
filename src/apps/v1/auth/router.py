from fastapi import APIRouter

from src.apps.v1.auth.schemas import UserLoginSchema, UserRegistrationSchema
from src.tags import AUTH_TAG

router = APIRouter(
    prefix="/auth",
    tags=[AUTH_TAG],
)


@router.post("/register")
def register(data: UserRegistrationSchema):
    return data


@router.post("/login_with_pass")
def login_with_pass(creds: UserLoginSchema):
    return {"Login with": creds}


@router.post("/refresh_access_token")
def refresh_access_token():
    return {"Refresh": "Access token"}


@router.post("/logout")
def logout():
    return "logout"
