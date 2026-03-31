from fastapi import APIRouter, UploadFile, File, Form, Depends, Cookie, HTTPException, BackgroundTasks
from pydantic import BaseModel
from core.services.chunk_service import ChunkService
from sqlalchemy.orm import Session
from data.clients.postgres_client import get_db
from data.repositories.video_repo import VideoRepository
from handlers.kafka.producer import publish_event
from config.settings import settings
from core.services.transcode_service import process_video_task
from handlers.search.index_video import index_video

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
    background_tasks: BackgroundTasks,
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

    try:
        # Index early so title search works immediately after upload.
        index_video(video)
    except Exception as exc:
        print("OpenSearch index error:", str(exc))

    publish_event(
        settings.kafka_topic,
        {
            "video_id": video.id,
            "user_id": video.owner_id,
            "s3_url": video.url,
        },
    )

    # Run local fallback processing so transcoding still happens even if Kafka topic is unavailable.
    background_tasks.add_task(
        process_video_task,
        {
            "video_id": video.id,
            "user_id": video.owner_id,
            "s3_url": video.url,
        },
    )

    # Cleanup temp files
    try:
        service.cleanup(filename)
    except Exception as e:
        print(f"Cleanup failed: {e}")

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