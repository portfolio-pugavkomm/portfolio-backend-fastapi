import pytest
from pydantic import SecretStr
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.apps.v1.auth.schemas import UserLoginSchema
from src.apps.v1.auth.services import CheckUserLoginCredsService


@pytest.mark.asyncio
async def test_should_return_false_for_non_created_user(db_session: AsyncSession) -> None:
    creds = UserLoginSchema(username="Some username", password=SecretStr("some password"))
    service = CheckUserLoginCredsService(creds, db_session)
    result = await service.execute()

    assert result is None


@pytest.mark.asyncio
async def test_should_return_false_for_wrong_data(db_session: AsyncSession) -> None:
    creds = UserLoginSchema(username="Some username", password=SecretStr("Wrong password"))
    service = CheckUserLoginCredsService(creds, db_session)
    result = await service.execute()

    assert result is None


@pytest.mark.asyncio
async def test_should_return_uuid_for_correct_creds(db_session: AsyncSession, created_user) -> None:  # type: ignore
    password = "paAsSw0r!d"
    created_user.password = password
    db_session.add(created_user)
    await db_session.commit()
    await db_session.refresh(created_user)

    creds = UserLoginSchema(username=created_user.username, password=SecretStr(password))
    service = CheckUserLoginCredsService(creds, db_session)
    result = await service.execute()

    assert result == created_user.user_uuid
