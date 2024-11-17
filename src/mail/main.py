from fastapi_mail import FastMail, ConnectionConfig
from jinja2 import Environment, FileSystemLoader
from src.config import Config
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

template_env = Environment(loader=FileSystemLoader("templates"))

mail_config = ConnectionConfig(
    MAIL_USERNAME=Config.MAIL_USERNAME,
    MAIL_PASSWORD=Config.MAIL_PASSWORD,
    MAIL_FROM=Config.MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER=Config.MAIL_SERVER,
    MAIL_FROM_NAME=Config.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(BASE_DIR, "templates"),
)


mail = FastMail(config=mail_config)
