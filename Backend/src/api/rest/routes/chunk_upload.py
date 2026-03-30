from fastapi import APIRouter, UploadFile, File, Form, Depends, Cookie, HTTPException
from sqlalchemy.orm import Session
from core.services.chunk_service import ChunkService
from data.clients.postgres_client import get_db
from data.repositories.video_repo import VideoRepository

router = APIRouter(prefix="/chunk", tags=["Chunk Upload"])

service = ChunkService()


# 🔥 STEP 1 — INIT
@router.post("/init")
def init_upload():
    upload_id = service.init_upload()
    return {"upload_id": upload_id}


# 🔥 STEP 2 — UPLOAD CHUNK
@router.post("/upload")
def upload_chunk(
    upload_id: str = Form(...),
    chunk_index: int = Form(...),
    file: UploadFile = File(...)
):
    service.save_chunk(upload_id, chunk_index, file)
    return {"status": "chunk received"}


# 🔥 STEP 3 — COMPLETE
@router.post("/complete")
def complete_upload(
    upload_id: str = Form(...),
    total_chunks: int = Form(...),
    title: str = Form(...),
    user_id: str = Cookie(None),
    db: Session = Depends(get_db)
):
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # merge chunks
    final_path = service.merge_chunks(upload_id, total_chunks)

    # upload to S3
    url = service.upload_to_s3(final_path)

    # save in DB
    repo = VideoRepository(db)
    video = repo.create_video({
        "title": title,
        "url": url,
        "owner_id": user_id
    })

    return {
        "id": video.id,
        "url": video.url
    }