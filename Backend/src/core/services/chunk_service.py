import os
import uuid
import shutil
from pathlib import Path
from handlers.storage.s3_client import S3Client


class ChunkService:
    def __init__(self):
        self.upload_dir = "uploads"
        self.s3 = S3Client()

        os.makedirs(self.upload_dir, exist_ok=True)

    def save_chunk(self, content: bytes, filename: str, chunk_index: int):
        """Save an individual chunk given its raw bytes."""
        chunk_dir = os.path.join(self.upload_dir, filename)
        os.makedirs(chunk_dir, exist_ok=True)

        chunk_path = os.path.join(chunk_dir, f"chunk_{chunk_index}")

        with open(chunk_path, "wb") as f:
            f.write(content)

        return chunk_path

    def merge_chunks(self, filename: str, total_chunks: int):
        """
        Merge all chunks into a single file
        """
        chunk_dir = os.path.join(self.upload_dir, filename)
        final_path = os.path.join(self.upload_dir, f"{filename}.mp4")

        with open(final_path, "wb") as final_file:
            for i in range(total_chunks):
                chunk_path = os.path.join(chunk_dir, f"chunk_{i}")

                with open(chunk_path, "rb") as chunk_file:
                    final_file.write(chunk_file.read())

        return final_path

    def upload_to_s3(self, final_path: str, filename: str):
        """
        Upload merged file to S3
        """
        # Use a safe generated key for S3 object name.
        # User-provided filenames can include spaces/special chars and extensions.
        base_name = Path(filename).stem or "video"
        object_name = f"{base_name}_{uuid.uuid4().hex}.mp4"
        s3_key = f"videos/{object_name}"

        url = self.s3.upload_file(final_path, s3_key)

        return url

    def cleanup(self, filename: str):
        """
        Remove chunks and merged file after upload
        """
        chunk_dir = os.path.join(self.upload_dir, filename)
        final_path = os.path.join(self.upload_dir, f"{filename}.mp4")

        # Remove chunk directory and all its contents
        if os.path.exists(chunk_dir):
            try:
                shutil.rmtree(chunk_dir)
            except Exception as e:
                print(f"Warning: Failed to remove chunk directory {chunk_dir}: {e}")

        # Remove merged file
        if os.path.exists(final_path):
            try:
                os.remove(final_path)
            except Exception as e:
                print(f"Warning: Failed to remove merged file {final_path}: {e}")