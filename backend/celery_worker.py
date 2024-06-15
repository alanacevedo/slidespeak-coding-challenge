
from app.utils.s3_utils import S3Manager
from celery import Celery
from io import BytesIO
from datetime import timedelta
from dotenv import load_dotenv
import os
import requests

load_dotenv()

celery = Celery(__name__)
celery.conf.broker_url = os.getenv("CELERY_BROKER_URL")
celery.conf.result_backend = os.getenv("CELERY_RESULT_BACKEND")

UNOSERVER_URL = os.getenv("UNOSERVER_URL")
PRESIGNED_URL_EXPIRATION_DAYS = os.getenv("PRESIGNED_URL_EXPIRATION_DAYS")

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")


@celery.task(name="convert_file_task")
def convert_file_and_upload__task(filename: str, converted_filename: str) -> str:
    """
    First downloads the powerpoint file from S3.
    Sends the file to unoserver via POST request to convert it to .pdf.
    Uploads the converted file to S3, generates a presigned URL, and then returns it.
    """

    s3_manager = S3Manager(
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_region=AWS_REGION,
        aws_s3_bucket_name=AWS_S3_BUCKET_NAME
    )

    file = s3_manager.download_file_from_s3(filename)

    form_data = {
        "convert-to": "pdf",
    }
    files = {
        "file": file
    }

    unoserver_endpoint = UNOSERVER_URL

    try:
        conversion_response = requests.post(unoserver_endpoint, data=form_data, files=files)
        conversion_response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        raise Exception(f"HTTP error: {str(exc)}")

    converted_file = BytesIO(conversion_response.content)

    expiration_seconds = int(timedelta(int(PRESIGNED_URL_EXPIRATION_DAYS)).total_seconds())

    s3_manager.upload_file_to_s3(converted_file, converted_filename)
    converted_file_url = s3_manager.generate_presigned_url(converted_filename, expiration_seconds)

    return converted_file_url
