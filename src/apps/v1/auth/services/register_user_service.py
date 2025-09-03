from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ..exceptions import UserNameAlreadyUsed
from ..models import UserModel
from ..schemas import UserRegistrationSchema, UserSchema


async def register_user_service(data: UserRegistrationSchema, ses: AsyncSession) -> UserSchema:
    new_user = UserModel(username=data.username, password=data.password.get_secret_value(), email=data.email)
    ses.add(new_user)
    try:
        await ses.commit()
    except IntegrityError:
        raise UserNameAlreadyUsed("Username or Email already exists")
    print(await ses.execute(select(UserModel)))
    return UserSchema.model_validate(new_user)
