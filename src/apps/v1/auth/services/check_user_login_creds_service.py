from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only

from src.apps.v1.auth.models import UserModel
from src.apps.v1.auth.schemas import UserLoginSchema


class CheckUserLoginCredsService:
    """Service for check user login credential data

    Args:
         cred: Credential data
         session: database async session
         is_active: if true check only active user. By default, true

    Returns:
        user uuid or None
    """

    Model = UserModel

    def __init__(self, cred: UserLoginSchema, session: AsyncSession, is_active: bool = True) -> None:
        self._cred = cred
        self._ses = session
        self._is_active = is_active

    async def _get_user_pass_hash(self) -> UUID | None:
        if user := (
            await self._ses.execute(
                select(UserModel)
                .filter_by(username=self._cred.username, is_active=self._is_active)
                .options(load_only(UserModel.user_uuid, UserModel.password_hash))
            )
        ).scalar_one_or_none():
            if user.verify_password(self._cred.password.get_secret_value()):
                return user.user_uuid
        return None

    async def execute(self) -> UUID | None:
        return await self._get_user_pass_hash()
