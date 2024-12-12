from datetime import datetime, timedelta
import uuid
import bcrypt
import jwt
import logging

from src.db.models import User
from src.config import Config


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password.decode("utf-8")


def create_confirmation_token(email: str) -> str:
    expire = datetime.now() + timedelta(minutes=Config.AUTH_EMAIL_CONFIRMATION_EXPIRES)
    data = {"exp": expire, "email": email}
    return jwt.encode(
        data, Config.AUTH_EMAIL_CONFIRMATION_SECRET, Config.AUTH_JWT_ALGORITHM
    )


def verify_confirmation_token(token: str) -> str | None:
    try:
        payload = jwt.decode(
            token,
            Config.AUTH_EMAIL_CONFIRMATION_SECRET,
            algorithms=[Config.AUTH_JWT_ALGORITHM],
        )
        return payload.get("email")
    except jwt.PyJWTError:
        return None


def sign_tokens(user: dict):
    access_token_exp = datetime.now() + timedelta(
        minutes=Config.AUTH_JWT_TOKEN_EXPIRES_IN
    )
    refresh_token_exp = datetime.now() + timedelta(
        minutes=Config.AUTH_REFRESH_TOKEN_EXPIRES_IN
    )

    access_token_payload = {
        "user": user,
        "exp": int(access_token_exp.timestamp()),
        "jti": str(uuid.uuid4()),
    }

    refresh_token_payload = {
        "user": user,
        "exp": int(refresh_token_exp.timestamp()),
        "jti": str(uuid.uuid4()),
    }

    access_token = jwt.encode(
        access_token_payload, Config.AUTH_JWT_SECRET, Config.AUTH_JWT_ALGORITHM
    )
    refresh_token = jwt.encode(
        refresh_token_payload, Config.AUTH_REFRESH_SECRET, Config.AUTH_JWT_ALGORITHM
    )

    return {"access_token": access_token, "refresh_token": refresh_token}


def verify_access_token(token: str):
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.AUTH_JWT_SECRET,
            algorithms=[Config.AUTH_JWT_ALGORITHM],
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None


def verify_refresh_token(token: str):
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.AUTH_REFRESH_SECRET,
            algorithms=[Config.AUTH_JWT_ALGORITHM],
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
