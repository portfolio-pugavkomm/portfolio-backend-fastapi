from uuid import UUID

from passlib.context import CryptContext
from sqlalchemy import ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base, pk_uuid, str_256

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000,
)


class UserModel(Base):
    __tablename__ = "users"
    user_uuid: Mapped[pk_uuid]
    username: Mapped[str] = mapped_column(String(length=100), unique=True)
    password_hash: Mapped[str_256] = mapped_column(name="password_hash")
    email: Mapped[str_256] = mapped_column(unique=True, nullable=True)
    # Is active can be use if blocked user
    is_active: Mapped[bool] = mapped_column(server_default=text("true"))
    role: Mapped[set["RoleModel"]] = relationship(secondary="user_role_association")

    @property
    def password(self) -> None:
        raise AttributeError("Password is not a readable")

    @password.setter
    def password(self, password: str) -> None:
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)

    def __repr__(self) -> str:
        return f"UUID({self.user_uuid}) username({self.username}) is_Active({self.is_active})"


class RoleModel(Base):
    __tablename__ = "roles"
    role_uuid: Mapped[pk_uuid]
    name: Mapped[str_256]


class UserRoleAssociationModel(Base):
    __tablename__ = "user_role_association"
    user_uuid: Mapped[UUID] = mapped_column(ForeignKey("users.user_uuid"), primary_key=True)  # TODO: rewrite with
    # pk_uuid
    role_uuid: Mapped[UUID] = mapped_column(ForeignKey("roles.role_uuid"), primary_key=True)
