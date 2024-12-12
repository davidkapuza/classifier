from fastapi import FastAPI
from src.auth.router import auth_router
from src.user.router import users_router
from src.auth.errors import register_auth_errors

version = "v1"

description = """
TODO
    """


version_prefix = f"/api/{version}"


app = FastAPI(
    title="Classifier",
    description=description,
    version=version,
    openapi_url=f"{version_prefix}/openapi.json",
    docs_url=f"{version_prefix}/docs",
    redoc_url=f"{version_prefix}/redoc",
)

register_auth_errors(app)

app.include_router(auth_router, prefix=f"{version_prefix}/auth", tags=["auth"])
app.include_router(users_router, prefix=f"{version_prefix}/users", tags=["users"])
