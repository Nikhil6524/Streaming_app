import boto3
from config.settings import settings


class S3Client:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region,
        )
        self.bucket = settings.aws_bucket_name

    def upload_file(self, file_obj, filename: str):
        self.s3.upload_fileobj(
            file_obj,
            self.bucket,
            filename,
            ExtraArgs={
                "ContentType": "video/mp4",   
                "ACL": "public-read"         
            }
        )

        return f"https://{self.bucket}.s3.{settings.aws_region}.amazonaws.com/{filename}"