from fastapi import FastAPI
from src.users.router import users_router

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


app.include_router(users_router, prefix=f"{version_prefix}/users", tags=["users"])
