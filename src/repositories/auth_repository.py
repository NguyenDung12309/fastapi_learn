from typing import Optional

from sqlmodel import Session
from sqlmodel import select

from src.models import UserModel
from src.models.token_model import TokenModel
from src.schemas.auth_schema import AccessTokenRequestSchema


class AuthRepository:
    def __init__(self, session: Session):
        self._session = session

    def register(self, user: UserModel):
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user

    def save_refresh_token(self, payload: TokenModel):
        self._session.add(payload)
        self._session.commit()
        self._session.refresh(payload)

    def get_refresh_token(self, payload: AccessTokenRequestSchema) -> Optional[TokenModel]:
        statement = select(TokenModel).where(
            TokenModel.refresh_token == payload.refresh_token,
            TokenModel.is_revoked == False
        )
        return self._session.exec(statement).first()

    def delete_refresh_token(self, payload: AccessTokenRequestSchema):
        data = self.get_refresh_token(payload)
        self._session.delete(data)
        self._session.commit()
