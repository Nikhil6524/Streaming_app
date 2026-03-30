from fastapi import APIRouter, UploadFile, File, Form, Depends, Cookie, HTTPException
from pydantic import BaseModel
from core.services.chunk_service import ChunkService
from sqlalchemy.orm import Session
from data.clients.postgres_client import get_db
from data.repositories.video_repo import VideoRepository

router = APIRouter(prefix="/chunk", tags=["Chunk Upload"])

service = ChunkService()


# =========================
# INIT (JSON-based)
# =========================
class InitRequest(BaseModel):
    filename: str


@router.post("/init")
def init_upload(req: InitRequest):
    """
    Initialize upload session
    """
    return {
        "message": "Upload initialized",
        "filename": req.filename
    }


# =========================
# UPLOAD CHUNK
# =========================
@router.post("/upload")
async def upload_chunk(
    file: UploadFile = File(...),
    filename: str = Form(...),
    chunk_index: int = Form(...)
):
    """
    Upload individual chunk
    """
    # Read file content from the async UploadFile and pass raw bytes
    content = await file.read()
    service.save_chunk(content, filename, chunk_index)

    return {
        "message": f"Chunk {chunk_index} uploaded"
    }


# =========================
# COMPLETE UPLOAD
# =========================
@router.post("/complete")
def complete_upload(
    filename: str = Form(...),
    total_chunks: int = Form(...),
    title: str = Form(...),
    user_id: str = Cookie(None),
    db: Session = Depends(get_db),
):
    """
    Merge chunks + upload to S3
    """
    # Merge chunks
    final_path = service.merge_chunks(filename, total_chunks)

    # Upload to S3
    url = service.upload_to_s3(final_path, filename)

    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Persist uploaded video so it appears in /videos feed
    repo = VideoRepository(db)
    video = repo.create_video(
        {
            "title": title,
            "url": url,
            "owner_id": user_id,
        }
    )

    # Cleanup temp files
    service.cleanup(filename)

    return {
        "message": "Upload complete",
        "id": video.id,
        "title": video.title,
        "url": video.url,
        "video_url": url,
        "quality_urls": {
            "360p": video.url,
            "480p": video.url,
            "720p": video.url,
        },
    }