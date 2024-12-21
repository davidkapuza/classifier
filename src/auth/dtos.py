from typing_extensions import Self
from pydantic import BaseModel, Field, field_validator, model_validator
from src.db.models import User


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


class ResetPasswordDto(BaseModel):
    email: str

    @field_validator("email")
    def normalize_email(cls, v):
        return v.lower()

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "johndoe123@co.com",
            }
        }
    }


class ResetPasswordConfirmationDto(BaseModel):
    new_password: str
    confirm_new_password: str

    @model_validator(mode="after")
    def passwords_match(self) -> Self:
        if self.new_password != self.confirm_new_password:
            raise ValueError("Passwords do not match")
        return self
