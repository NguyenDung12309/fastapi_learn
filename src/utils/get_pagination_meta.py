import math
from typing import Type, Any
from sqlmodel import Session, select, func, SQLModel


def get_pagination_metadata(session: Session, model: Type[SQLModel], page: int, page_size: int):
    count_statement = select(func.count()).select_from(model)
    total_count = session.exec(count_statement).one()

    total_pages = math.ceil(total_count / page_size) if total_count > 0 else 0

    return total_count, total_pages