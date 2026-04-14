from typing import Optional

from sqlmodel import Session
from sqlmodel import select

from src.models import UserModel
from src.models.token_model import TokenModel


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

    def get_refresh_token(self, refresh_token: str) -> Optional[TokenModel]:
        statement = select(TokenModel).where(
            TokenModel.refresh_token == refresh_token,
        )
        return self._session.exec(statement).first()

    def revoke_refresh_token(self, refresh_token: str):
        data = self.get_refresh_token(refresh_token)
        if data:
            data.is_revoked = True
        self._session.add(data)
        self._session.commit()
