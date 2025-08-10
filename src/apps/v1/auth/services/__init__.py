from sqlalchemy.ext.asyncio import AsyncSession
from src.apps.v1.auth.models import UserModel

from src.apps.v1.auth.schemas import UserLoginSchema


class CheckUserLoginCredsService:
    Model = UserModel
    def __init__(self, cred: UserLoginSchema, session: AsyncSession) -> None:
        self._cred = cred
        self._ses = session

    def _get_user_pass_hash(self) -> str | None:
        user = self._ses.execute(UserModel.)

    def execute(self) -> bool:
