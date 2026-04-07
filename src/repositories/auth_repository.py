from sqlmodel import Session

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
