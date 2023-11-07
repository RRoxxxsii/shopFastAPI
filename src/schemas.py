from pydantic import BaseModel


class BaseUser(BaseModel):

    id: int
    name: str
    surname: str
    email: str
    email_confirmed: bool
