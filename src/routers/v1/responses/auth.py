from datetime import datetime

from pydantic import BaseModel, EmailStr


class RegisterUserOut(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    time_created: datetime
    email_confirmed: bool
    is_admin: bool
    is_stuff: bool


class TokenOut(BaseModel):
    access_token: str
