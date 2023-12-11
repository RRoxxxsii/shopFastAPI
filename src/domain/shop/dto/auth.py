from pydantic import BaseModel, EmailStr


class UserDTO(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password1: str


class AuthDTO(BaseModel):
    email: str
    password: str

