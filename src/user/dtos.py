from pydantic import BaseModel, Field, field_validator
from src.db.models import User

class CreateUserDto(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)

    @field_validator("email")
    def normalize_email(cls, v):
        return v.lower()

    model_config = {
        "json_schema_extra": {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "username": "johndoe",
                "email": "johndoe123@co.com",
                "password": "testpass123",
            }
        }
    }


class LoginDto(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)

    @field_validator("email")
    def normalize_email(cls, v):
        return v.lower()

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "johndoe123@co.com",
                "password": "testpass123",
            }
        }
    }


class LoginResponseDto(BaseModel):
    access_token: str
    refresh_token: str
    user: User