import boto3
from botocore.exceptions import ClientError
from botocore.client import Config
from datetime import datetime
import uuid
from config import config

class S3Uploader:
    """Handle S3/Allas uploads"""

    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            endpoint_url=config.ALLAS_ENDPOINT,
            region_name="eu-north-1",
            aws_access_key_id=config.ALLAS_ACCESS_KEY,
            aws_secret_access_key=config.ALLAS_SECRET_KEY,
            config=Config(s3={'addressing_style': 'path'})
        )

    def upload_image(self, file_bytes: bytes, original_filename: str = None) -> str:
        """Upload image to S3 and return URL"""
        try:
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            filename = f"toothpaste_{timestamp}_{unique_id}.webp"

            # Upload to S3
            self.s3_client.put_object(
                Bucket=config.ALLAS_BUCKET,
                Key=filename,
                Body=file_bytes,
                ContentType="image/webp",
                ACL="public-read"
            )

            # Construct public URL
            upload_url = f"{config.ALLAS_ENDPOINT}/{config.ALLAS_BUCKET}/{filename}"
            return upload_url

        except ClientError as e:
            raise Exception(f"S3 upload failed: {str(e)}")

