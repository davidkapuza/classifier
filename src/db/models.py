from datetime import datetime

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, SQLModel

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int = Field(sa_column=Column(pg.INTEGER, primary_key=True, autoincrement=True))
    username: str
    email: str
    first_name: str
    last_name: str
    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
    )
    is_verified: bool = Field(default=False)
    password_hash: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False), exclude=True
    )
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def model_dump(self, **kwargs):
        dump = super().model_dump(**kwargs)
        dump["created_at"] = self.created_at.isoformat() if self.created_at else None
        dump["updated_at"] = self.updated_at.isoformat() if self.updated_at else None
        return dump
