from ..utils.s3_utils import S3Manager
from fastapi import UploadFile, HTTPException
from datetime import timedelta
from httpx import AsyncClient, HTTPError
from dotenv import load_dotenv
from io import BytesIO
from uuid import uuid4
from datetime import datetime
import os

load_dotenv()

UNOSERVER_URL = os.getenv("UNOSERVER_URL")
PRESIGNED_URL_EXPIRATION_DAYS = os.getenv("PRESIGNED_URL_EXPIRATION_DAYS")

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")


async def convert_file(file: UploadFile) -> BytesIO:
    """
    Sends the powerpoint file to unoserver to convert it to .pdf via POST request
    and returns the converted file as BytesIO.
    """

    form_data = {
        "convert-to": (None, "pdf"),
        "file": (file.filename, file.file, file.content_type)
    }

    unoserver_endpoint = UNOSERVER_URL

    async with AsyncClient() as client:
        try:
            conversion_response = await client.post(unoserver_endpoint, files=form_data)
            conversion_response.raise_for_status()
        except HTTPError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=str(exc))

    converted_file_data = conversion_response.content
    converted_file = BytesIO(converted_file_data)

    file.file.seek(0)

    return converted_file


async def convert_and_share(file: UploadFile):
    """
    Converts the powerpoint file to a pdf file with the unoserver API.
    Uploads both files to S3, and then generates and returns presigned url for the converted file.
    """

    converted_file = await convert_file(file)

    s3_manager = S3Manager(
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_region=AWS_REGION,
        aws_s3_bucket_name=AWS_S3_BUCKET_NAME
    )

    filename, converted_filename = get_filenames(file.filename)

    s3_manager.upload_file_to_s3(file.file, filename)
    s3_manager.upload_file_to_s3(converted_file, converted_filename)

    expiration_seconds = int(timedelta(int(PRESIGNED_URL_EXPIRATION_DAYS)).total_seconds())
    converted_file_url = s3_manager.generate_presigned_url(converted_filename, expiration_seconds)

    return {
        "converted_file_url": converted_file_url
    }


def get_filenames(original_filename: str) -> tuple[str, str]:
    """
    Given a filename, returns a new unique filename based on current time and UUID.
    Also returns the filename for the converted file, ending in ".pdf".
    """
    now = datetime.now().strftime("%Y-%m-%d")
    file_id = uuid4().hex[:6]

    splitted_filename = original_filename.split(".")
    prefix = ".".join(splitted_filename[:-1])
    extension = splitted_filename[-1]

    filename = f"{prefix}_{now}_{file_id}.{extension}"
    converted_filename = f"converted_{prefix}_{now}_{file_id}.pdf"

    return filename, converted_filename
