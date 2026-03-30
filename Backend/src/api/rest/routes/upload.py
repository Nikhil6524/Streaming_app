from fastapi import APIRouter, UploadFile, File, Form, Depends, Cookie, HTTPException
from sqlalchemy.orm import Session
from data.clients.postgres_client import get_db
from data.repositories.video_repo import VideoRepository
from core.services.video_service import VideoService

router = APIRouter(prefix="/upload", tags=["Upload"])


def get_video_service(db: Session = Depends(get_db)):
    repo = VideoRepository(db)
    return VideoService(repo)


@router.post("/")
def upload_video(
    file: UploadFile = File(...),
    title: str = Form(...),
    user_id: str = Cookie(None),
    service: VideoService = Depends(get_video_service),
):
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    #  VALIDATION 1: Check MIME type
    if file.content_type != "video/mp4":
        raise HTTPException(status_code=400, detail="Only MP4 files are allowed")

    video = service.upload_video(file, user_id, title)

    return {
        "id": video.id,
        "url": video.url
    }