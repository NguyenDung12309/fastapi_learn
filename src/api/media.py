from fastapi import APIRouter, UploadFile, File, Depends

from src.common.enum_common import PermissionKey
from src.core.dependency import access_token_bear_depend, PermissionChecker
from src.schemas.media_schema import ImageUploadResponseSchema
from src.services.media_service import MediaService

media_router = APIRouter(prefix="/media", tags=["Media"])


@media_router.post("/upload", dependencies=[Depends(access_token_bear_depend),
                                            Depends(PermissionChecker(
                                                PermissionKey.UPLOAD_MEDIA))],
                   response_model=ImageUploadResponseSchema)
async def upload_image(payload: UploadFile = File(...)):
    return MediaService.upload(payload)
