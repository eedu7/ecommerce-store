from datetime import datetime

import boto3
from botocore.exceptions import NoCredentialsError
from fastapi import UploadFile

from core.config import config
from core.exceptions import UnauthorizedException


class S3ImageManager:
    s3 = boto3.client("s3", config.AWS_REGION)
    bucket_name = config.AWS_BUCKET_NAME

    @staticmethod
    async def upload_image(file: UploadFile, file_name: str) -> bool:
        """
        Upload a file to an S3 bucket
        :param file: FastAPI UploadFile object
        :param file_name: Name of the file to be uploaded
        """

        try:
            S3ImageManager.s3.upload_fileobj(
                file.file,
                S3ImageManager.bucket_name,
                file_name,
            )
            return True
        except NoCredentialsError:
            raise UnauthorizedException("AWS credentials not available")
        return False

    @staticmethod
    def construct_file_name(file_name: str) -> str:
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        return f"{timestamp}_{file_name}"

    @staticmethod
    async def get_presigned_url(file_name: str, expiration: int = 3600) -> str:
        try:
            url = S3ImageManager.s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": S3ImageManager.bucket_name, "Key": file_name},
                ExpiresIn=expiration,
            )
            return url
        except NoCredentialsError:
            raise UnauthorizedException("AWS credentials not available")
