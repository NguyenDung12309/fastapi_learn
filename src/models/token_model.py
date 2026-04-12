from datetime import datetime
from uuid import UUID

from sqlalchemy import Column, DateTime
from sqlmodel import Field

from src.models.base_table_model import BaseTableModel


class TokenModel(BaseTableModel, table=True):
    __tablename__ = 'token'

    user_id: UUID = Field(foreign_key="user.id")
    refresh_token: str = Field(index=True)
    is_revoked: bool = Field(default=False)
    expires_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
