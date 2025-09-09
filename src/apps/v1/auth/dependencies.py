from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.apps.v1.auth.bearers import JWTBearer
from src.apps.v1.auth.defs import RolesEnum
from src.apps.v1.auth.models import UserModel
from src.apps.v1.auth.services import decode_jwt_service
from src.dependencies import DBSessionDep

jwt_bearer = JWTBearer()


async def dep_get_current_user(
    ses: DBSessionDep,
    creds: HTTPAuthorizationCredentials = Depends(jwt_bearer),
) -> UserModel:
    payload = decode_jwt_service(creds.credentials)
    # payload is not none, because JWTBearer already checked
    user_id = payload.get("user_id")  # type: ignore
    q = select(UserModel).filter_by(user_uuid=user_id).options(selectinload(UserModel.role))
    user = (await ses.execute(q)).scalar_one_or_none()
    if user is None:
        raise HTTPException(403, detail="User not found")

    return user


class RoleChecker:
    def __init__(self, allowed_roles: set[str]):
        self.allowed_roles = allowed_roles

    async def __call__(self, user: UserModel = Depends(dep_get_current_user)) -> UserModel:
        if not ({r.name for r in user.role} & self.allowed_roles):
            raise HTTPException(status_code=403, detail="You do not have permission to access this resource.")
        return user


admin_required = RoleChecker({RolesEnum.admin})
