from uuid import UUID

from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from typing import Sequence
from src.book.schemas import BookCreateReq, BookUpdateReq

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
        exec_query = await session.execute(statement)
        result = exec_query.scalar_one_or_none()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        return result

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
        if book_info:
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
