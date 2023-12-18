from sqladmin import ModelView

from src.infrastructure.database.models.auth import Token, User


class UserAdmin(ModelView, model=User):  # type: ignore
    column_list = [
        User.id,
        User.name,
        User.surname,
        User.email,
        User.time_created,
        User.is_admin,
        User.is_partner,
        User.email_confirmed,
        User.is_stuff,
        User.partner,
    ]


class TokenAdmin(ModelView, model=Token):  # type: ignore
    column_list = [Token.id, Token.user_id]
