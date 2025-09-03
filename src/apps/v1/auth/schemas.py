from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr


class UserLoginSchema(BaseModel):
    username: str = Field(...)
    password: SecretStr = Field(...)

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "username": "username1",
                    "password": "pAasW0r!d",
                },
            ]
        }
    )


class UserRegistrationSchema(UserLoginSchema):
    email: EmailStr | None = Field(None)

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "username": "username1",
                    "password": "pAasW0r!d",
                    "email": "email@example.com",
                }
            ]
        }
    )


class UserSchema(BaseModel):
    username: str = Field(...)
    email: EmailStr | None = Field(None)

    model_config = ConfigDict(from_attributes=True)


class JWTTokenResponseSchema(BaseModel):
    access: str
    refresh: str | None


class RefreshTokenSchema(BaseModel):
    refresh: str = Field(...)
