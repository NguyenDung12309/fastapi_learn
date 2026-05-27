from fastapi import APIRouter, UploadFile, File

from src.schemas.media_schema import ImageUploadResponseSchema
from src.services.media_service import MediaService

media_router = APIRouter(prefix="/media", tags=["Media"])


@media_router.post("/upload", response_model=ImageUploadResponseSchema)
async def upload_image(payload: UploadFile = File(...)):
    return MediaService.upload(payload)
