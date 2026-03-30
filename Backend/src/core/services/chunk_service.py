import os
import uuid
from handlers.storage.s3_client import S3Client

UPLOAD_DIR = "tmp/uploads"


class ChunkService:
    def __init__(self):
        self.s3 = S3Client()

    def init_upload(self):
        upload_id = str(uuid.uuid4())
        path = os.path.join(UPLOAD_DIR, upload_id)
        os.makedirs(path, exist_ok=True)
        return upload_id

    def save_chunk(self, upload_id: str, chunk_index: int, file):
        path = os.path.join(UPLOAD_DIR, upload_id)
        chunk_path = os.path.join(path, f"chunk_{chunk_index}")

        with open(chunk_path, "wb") as f:
            f.write(file.file.read())

    def merge_chunks(self, upload_id: str, total_chunks: int):
        path = os.path.join(UPLOAD_DIR, upload_id)
        final_file_path = os.path.join(path, "final.mp4")

        with open(final_file_path, "wb") as final_file:
            for i in range(total_chunks):
                chunk_path = os.path.join(path, f"chunk_{i}")
                with open(chunk_path, "rb") as chunk_file:
                    final_file.write(chunk_file.read())

        return final_file_path

    def upload_to_s3(self, file_path: str):
        filename = f"{uuid.uuid4()}.mp4"

        with open(file_path, "rb") as f:
            url = self.s3.upload_file(f, filename)

        return url