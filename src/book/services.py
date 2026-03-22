from uuid import UUID
from fastapi import HTTPException, status
from typing import Sequence
from src.book.schemas import BookCreateReq, BookUpdateReq
from src.book.models import BookModel
from sqlmodel import Session, select, desc

class BookService:
    @staticmethod
    def get_all_book(session: Session) -> Sequence[BookModel]:
        statement = select(BookModel).order_by(desc(BookModel.created_at))
        result = session.exec(statement)
        return result.all()

    @staticmethod
    def get_book_by_id( book_uid: UUID, session: Session) -> BookModel:
        statement = select(BookModel).where(BookModel.id == book_uid)
        exec_query = session.exec(statement)
        result = exec_query.one_or_none()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        return result

    @staticmethod
    def create_book(payload: BookCreateReq, session: Session) -> BookModel:
        dump_data = payload.model_dump()
        result = BookModel(**dump_data)
        session.add(result)
        session.commit()
        session.refresh(result)
        return result

    def update_book(self, book_uid: UUID, payload: BookUpdateReq, session: Session) -> BookModel:
        book_info = self.get_book_by_id(book_uid, session)
        dump_data = payload.model_dump()
        if book_info:
            for key, value in dump_data.items():
                setattr(book_info, key, value)
            session.commit()
            session.refresh(book_info)
        return book_info

    def delete_book(self, book_uid: UUID, session: Session):
        book_info = self.get_book_by_id(book_uid, session)
        session.delete(book_info)
        session.commit()
