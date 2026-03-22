from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from typing import Sequence
from src.book.schemas import Book, BookCreateReq, BookUpdateReq

from src.book.models import BookModel

class BookService:
    @staticmethod
    async def get_all_book(session: AsyncSession) -> Sequence[BookModel]:
        statement = select(BookModel).order_by(desc(BookModel.created_at))
        result = await session.execute(statement)
        return result.scalars().all()

    @staticmethod
    async def get_book_by_id( book_uid: UUID, session: AsyncSession) -> BookModel:
        statement = select(BookModel).where(BookModel.id == book_uid)
        result = await session.execute(statement)

        return result.scalar_one_or_none()

    @staticmethod
    async def create_book(payload: BookCreateReq, session: AsyncSession) -> BookModel:
        dump_data = payload.model_dump()
        result = BookModel(**dump_data)
        session.add(result)
        await session.commit()
        return result

    async def update_book(self, book_uid: UUID, payload: BookUpdateReq, session: AsyncSession) -> BookModel:
        book_info = await self.get_book_by_id(book_uid, session)
        dump_data = payload.model_dump()
        for key, value in dump_data.items():
            setattr(book_info, key, value)
        await session.commit()
        return book_info

    async def delete_book(self, book_uid: UUID, session: AsyncSession) -> BookModel:
        book_info = await self.get_book_by_id(book_uid, session)
        if book_info:
            await session.delete(book_info)
            await session.commit()
        return book_info
