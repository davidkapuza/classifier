from fastapi import FastAPI, status

from src.shared.utils import create_exception_handler


class AuthException(Exception):
    pass


class UserAlreadyExists(AuthException):
    pass


class InvalidCredentials(AuthException):
    pass


class AccountNotVerified(AuthException):
    pass


class InvalidVerificationToken(AuthException):
    pass


class Unauthorized(AuthException):
    pass


def register_auth_errors(app: FastAPI):
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        ),
    )

    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        ),
    )

    app.add_exception_handler(
        AccountNotVerified,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account requires verification",
        ),
    )

    app.add_exception_handler(
        InvalidVerificationToken,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            detail="Invalid verification token",
        ),
    )

    app.add_exception_handler(
        Unauthorized,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
        ),
    )
