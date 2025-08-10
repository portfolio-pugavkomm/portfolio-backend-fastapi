from pydantic import BaseModel, EmailStr, Field, Secret


class UserLoginSchema(BaseModel):
    username: str = Field(...)
    password: Secret[str] = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "username1",
                "password": "pAasW0r!d",
            }
        }


class UserRegistrationSchema(UserLoginSchema):
    email: EmailStr = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "username1",
                "password": "pAasW0r!d",
                "email": "email@example.com",
            }
        }
