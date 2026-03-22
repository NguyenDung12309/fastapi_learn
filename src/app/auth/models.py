import uuid
from uuid import UUID
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import SQLModel, Field,Column
from sqlalchemy import func

class UserModel(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4,
        )
    )
    username: str = Field(unique=True, index=True)
    email: str
    first_name: str
    last_name: str
    is_verified: bool = Field(
       default=False
    )
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, server_default=func.now())
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, server_default=func.now(), onupdate=func.now())
    )

    def __repr__(self):
        return f"<User {self.username}>"