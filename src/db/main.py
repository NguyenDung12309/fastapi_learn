from sqlalchemy.ext.asyncio import  create_async_engine
from sqlalchemy.util import await_only

from src.config import Config
from sqlmodel import text, SQLModel

engine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True,
)

async def init_db():
    async with engine.begin() as conn:
        from src.book.models import BookBase
        await conn.run_sync(SQLModel.metadata.create_all)