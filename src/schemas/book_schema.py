from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field

from src.models import BookModel


# Giả sử bạn định nghĩa BookStatus Enum ở common hoặc import đúng từ model


class CreateBookRequestSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Tiêu đề sách")
    author_name: str = Field(..., min_length=1, description="Tên tác giả")
    description: str = Field(..., description="Mô tả nội dung sách")
    publisher_id: UUID
    category_ids: List[UUID] = Field(default=[], description="Danh sách ID của các danh mục")

    image: Optional[str] = None
    status: BookModel.BookStatus = Field(default=BookModel.BookStatus.ONGOING)
    rating: int = Field(default=0, ge=0, le=5, description="Đánh giá từ 0 đến 5 sao")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "title": "Chí Phèo",
                "author_name": "Nam Cao",
                "description": "Một tác phẩm văn học hiện thực xuất sắc.",
                "publisher_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "category_ids": ["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
                "image": "https://example.com/cover.jpg",
                "status": "draft",
                "rating": 5
            }
        }
