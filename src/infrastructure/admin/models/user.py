from sqladmin import ModelView

from src.infrastructure.database.models.auth import User, Token


class UserAdmin(ModelView, model=User):
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
        User.partner
    ]


class TokenAdmin(ModelView, model=Token):
    column_list = [
        Token.id,
        Token.user_id
    ]
