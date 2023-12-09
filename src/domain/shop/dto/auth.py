from pydantic import BaseModel, EmailStr


class CreateUserDTO(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password1: str


class AuthDTO(BaseModel):
    email: str
    password: str


class UserDTO(BaseModel):
    name: str
    surname: str
    email: EmailStr
    hashed_password: str


class TokenDTO(BaseModel):
    access_token: str
    user_id: int
