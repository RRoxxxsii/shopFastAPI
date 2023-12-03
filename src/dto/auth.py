from pydantic import BaseModel, EmailStr


class UserDTO(BaseModel):
    name: str
    surname: str
    email: EmailStr
    hashed_password: str


class TokenDTO(BaseModel):
    access_token: str
    user_id: int
