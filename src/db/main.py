from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.config import Config
from sqlmodel import text, SQLModel

engine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True,
)

async def init_db():
    async with engine.begin() as conn:
        from src.book.models import BookModel
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    Session = async_sessionmaker(bind=engine,
                           class_=AsyncSession,
                           expire_on_commit=False)

    async with Session() as session:
        yield session