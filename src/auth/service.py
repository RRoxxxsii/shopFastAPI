from src.auth.crud import CreateTokenCRUD, RegisterUserCrud


class AuthService(CreateTokenCRUD, RegisterUserCrud):

    def send_confirmation_email(self, email: str):
        raise NotImplementedError('SMTP has not been configured')
