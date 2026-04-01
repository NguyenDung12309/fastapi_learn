from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session

from src.core.config import Config


class DatabaseManager:
    def __init__(self):
        self._engine = create_engine(Config.database_url, echo=True)
        self._session_factory = sessionmaker(bind=self.engine, class_=Session, expire_on_commit=False)

    @property
    def engine(self) -> Engine:
        return self._engine

    def get_db(self):
        with self._session_factory() as session:
            yield session

    def close_connections(self):
        self._engine.dispose()


db_manager = DatabaseManager()
