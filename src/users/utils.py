from datetime import datetime, timedelta
import bcrypt
import jwt


from src.config import Config


def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_byte_enc = plain_password.encode("utf-8")
    return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password)


def get_password_hash(password: str) -> bytes:
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password


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
