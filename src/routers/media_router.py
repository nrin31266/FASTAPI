from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from typing import List

from src import dto
from src.database import get_db
from src.dto import ApiResponse
from src.services import media_service
from src.keycloak_auth.dto import UserPrincipal
from src.keycloak_auth.dependencies import get_current_user, require_roles
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/media", tags=["media"])


@router.post("/download/audio", response_model=ApiResponse[dto.MediaAudioResponse], status_code=status.HTTP_202_ACCEPTED)
def download_youtube_audio(
    rq: dto.MediaAudioCreateRequest,
    db: Session = Depends(get_db),
    # current_user: UserPrincipal = Depends(require_roles(["ROLE_ADMIN"])),
):
    # logger.info(f"User {current_user.username} is downloading audio from {rq.input_url} with type {rq.input_type}")
    media_audio = media_service.download_audio(rq, db)

    return ApiResponse.success(data=media_audio)

@router.post("/download/audio_url", response_model=ApiResponse[dto.AudioInfo], status_code=status.HTTP_202_ACCEPTED)
def download_audio_url(
    audio_url: str,
    # current_user: UserPrincipal = Depends(require_roles(["ROLE_ADMIN"])),
):
    # logger.info(f"User {current_user.username} is downloading audio from {rq.input_url} with type {rq.input_type}")
    audio_info = media_service.download_audio_file(audio_url)

    return ApiResponse.success(data=audio_info)