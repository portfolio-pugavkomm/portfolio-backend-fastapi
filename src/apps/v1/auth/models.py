from uuid import UUID, uuid4

from passlib.context import CryptContext
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base, pk_uuid, str_256
from sqlalchemy import text

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000,
)


class UserModel(Base):
    __tablename__ = "user"
    user_uuid: Mapped[pk_uuid]
    username: Mapped[str] = mapped_column(String(length=100), unique=True)
    password_hash: Mapped[str_256] = mapped_column(name="password_hash")
    email: Mapped[str_256] = mapped_column(unique=True, nullable=True)
    # Is active can be use if blocked user
    is_active: Mapped[bool] = mapped_column(server_default=text("true"))

    @property
    def password(self) -> None:
        raise AttributeError("Password is not a readable")

    @password.setter
    def password(self, password: str) -> None:
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)
