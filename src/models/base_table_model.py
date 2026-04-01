from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import func, text
from sqlmodel import Field, SQLModel


class BaseTableModel(SQLModel):
    id: Optional[UUID] = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
        sa_column_kwargs={
            "server_default": text("gen_random_uuid()"),
        }
    )
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column_kwargs={
            "server_default": func.now(),
        }
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column_kwargs={
            "server_default": func.now(),
            "onupdate": func.now(),
        }
    )
