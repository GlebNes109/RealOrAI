from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field


class Role(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"

class UsersDB(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: str = Field(primary_key=True)
    login: str = Field(unique=True)
    password_hash: str
    role: Optional[Role] = Role.USER