from passlib.context import CryptContext
import bcrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify_password_hash(raw_password, hashed_password):
    return pwd_context.verify(raw_password, hashed_password)


def custom_password_hash(raw_password):

    return pwd_context.hash(raw_password)