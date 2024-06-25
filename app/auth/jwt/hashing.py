from passlib.context import CryptContext
from passlib.exc import PasswordValueError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> None:
    """
    check if plain_password matches hashed_password, raise PasswordValueError if not.
    """
    if not pwd_context.verify(plain_password, hashed_password):
        raise PasswordValueError()


def get_password_hash(password: str) -> str:
    """
    generate hashed password with
    """
    return pwd_context.hash(password)
