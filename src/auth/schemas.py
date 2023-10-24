from pydantic import BaseModel, EmailStr, field_validator, model_validator
from sqlalchemy.orm import Session

from src.models import User as UserModel

db = Session()


class User(BaseModel):
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

    @classmethod
    @field_validator('email')
    def validate_email_taken(cls):
        email = cls.email
        query = db.query(UserModel).filter(UserModel.email == email).first()
        if query:
            raise ValueError('Email already exists')
        return cls
