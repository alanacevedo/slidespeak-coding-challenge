import boto3
from botocore.exceptions import ClientError, EndpointConnectionError, ParamValidationError
from fastapi import HTTPException
from typing import BinaryIO
from io import BytesIO


class S3Manager:
    """
    A class to manage interaction with S3 bucket.
    """
    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str, aws_region: str, aws_s3_bucket_name: str) -> None:
        """
        Initializes the S3 client with provided credentials.

        Args:
        aws_access_key_id (str): Your AWS access key ID.
        aws_secret_access_key (str): Your AWS secret access key.
        aws_region (str): The region where your S3 bucket resides.
        aws_s3_bucket_name (str): The name of your S3 bucket.
        """
        try:
            self.s3_client = boto3.client(
                service_name="s3",
                region_name=aws_region,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key
            )
        except (ClientError, EndpointConnectionError, ParamValidationError) as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=str(exc))

        self.bucket_name = aws_s3_bucket_name

    def upload_file_to_s3(self, file: BinaryIO, filename: str) -> None:
        """
        Uploads a file to the S3 bucket.

        Args:
        file (BytesIO): The file object or path to the file to upload.
        filename (str): The filename to use for the uploaded object in S3.
        """
        try:
            self.s3_client.upload_fileobj(file, self.bucket_name, filename)

        except ClientError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=str(exc))

        return

    def download_file_from_s3(self, filename: str) -> BytesIO:
        """
        Downloads a file from the S3 bucket.

        Args:
        filename (str): The filename of the object to download from S3.

        Returns:
        BytesIO: The downloaded file content as a BytesIO object.
        """
        try:
            file = BytesIO()
            self.s3_client.download_fileobj(self.bucket_name, filename, file)
            file.seek(0)

        except ClientError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=str(exc))

        return file

    def generate_presigned_url(self, filename: str, expiration_seconds: int) -> str:
        """
        Generates a presigned URL for an already existing file in S3 bucket.

        Args:
        filename (str): The filename of the object in S3.
        expiration_seconds (int): The number of seconds the presigned URL will be valid for.

        Returns:
        str: The generated presigned URL.
        """
        params = {
            "Bucket": self.bucket_name,
            "Key": filename,
        }

        try:
            file_url: str = str(self.s3_client.generate_presigned_url("get_object",
                                                                      Params=params,
                                                                      ExpiresIn=expiration_seconds))

        except ClientError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=str(exc))

        return file_url
