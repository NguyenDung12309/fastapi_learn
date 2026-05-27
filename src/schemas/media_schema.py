from pydantic import BaseModel


class ImageUploadResponseSchema(BaseModel):
    image_url: str
