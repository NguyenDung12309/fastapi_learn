from src.config import Config
from sqlmodel import SQLModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session

engine = create_engine(
    url=Config.DATABASE_URL,
    echo=True,
)

def init_db():
    from src.book.models import BookModel
    SQLModel.metadata.create_all(bind=engine)

def get_session():
    session_local = sessionmaker(
        bind=engine,
        class_=Session,
        expire_on_commit=False
    )

    with session_local() as session:
        yield session