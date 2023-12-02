from datetime import datetime

from pydantic import BaseModel, EmailStr, model_validator


class RegisterUserIn(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password1: str
    password2: str

    @model_validator(mode='after')
    def check_passwords_match(self):
        pw1 = self.password1
        pw2 = self.password2

        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('Passwords do not match..')
        return self


class UserSchema(BaseModel):
    name: str
    surname: str
    email: EmailStr
    hashed_password: str


class RegisterUserOut(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    time_created: datetime
    email_confirmed: bool
    is_admin: bool
    is_stuff: bool


class LoginUserIn(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
