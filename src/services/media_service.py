import cloudinary
import cloudinary.uploader
from fastapi import UploadFile, HTTPException, status

from src.core.config import Config
from src.schemas.media_schema import ImageUploadResponseSchema

cloudinary.config(
    cloud_name=Config.CLOUD_NAME,
    api_key=Config.CLOUD_KEY,
    api_secret=Config.CLOUD_SECRET,
    secure=True
)


class MediaService:
    @staticmethod
    def upload(file: UploadFile) -> ImageUploadResponseSchema:
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Định dạng file không hợp lệ. Hệ thống chỉ chấp nhận file hình ảnh (jpg, png, webp...)."
            )

        try:
            upload_result = cloudinary.uploader.upload(
                file.file,
                folder="book_management_covers"
            )

            secure_url = upload_result.get("secure_url")

            if not secure_url:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Không thể lấy được liên kết ảnh từ hệ thống lưu trữ."
                )

            return ImageUploadResponseSchema(image_url=secure_url)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Xảy ra lỗi trong quá trình upload: {str(e)}"
            )
