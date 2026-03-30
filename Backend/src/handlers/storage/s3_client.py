import boto3
from config.settings import settings
from urllib.parse import urlparse, unquote


class S3Client:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region,
            endpoint_url=f"https://s3.{settings.aws_region}.amazonaws.com",
        )
        self.bucket = settings.aws_bucket_name

    def upload_file(self, local_path: str, s3_key: str):
        """
        Upload file to S3 using file path
        """
        if hasattr(local_path, "read"):
            # Support file-like objects (e.g. FastAPI UploadFile.file)
            self.s3.upload_fileobj(local_path, self.bucket, s3_key)
        else:
            self.s3.upload_file(local_path, self.bucket, s3_key)

        encoded_key = s3_key.replace(" ", "%20").replace("(", "%28").replace(")", "%29")

        return f"https://{self.bucket}.s3.{settings.aws_region}.amazonaws.com/{encoded_key}"

    def get_s3_key_from_url(self, url: str):
        """Extract S3 object key from a virtual-hosted style S3 URL."""
        if not url:
            return None

        parsed = urlparse(url)
        path = parsed.path.lstrip("/")

        if not path:
            return None

        return unquote(path)

    def generate_presigned_url(self, s3_key: str, expires_in: int = 3600):
        return self.s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": s3_key},
            ExpiresIn=expires_in,
        )

    def download_file(self, s3_key: str, local_path: str):
        self.s3.download_file(self.bucket, s3_key, local_path)