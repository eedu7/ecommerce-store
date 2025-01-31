from passlib.context import CryptContext


class PasswordHandler:
    pwd_context = CryptContext(schemes=["bcrypt"], depracted="auto")

    @staticmethod
    def hash(password: str) -> str:
        return PasswordHandler.pwd_context.hash(password)

    @staticmethod
    def verify(hashed_password: str, plain_password: str) -> bool:
        return PasswordHandler.pwd_context.verify(plain_password, hashed_password)
