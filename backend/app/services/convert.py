import os
from ..utils.s3_utils import S3Manager
from fastapi import HTTPException, UploadFile
from dotenv import load_dotenv
from uuid import uuid4
from datetime import datetime
from celery_app.tasks import convert_file_and_upload__task
from celery.result import AsyncResult

load_dotenv()

UNOSERVER_URL = os.getenv("UNOSERVER_URL")
PRESIGNED_URL_EXPIRATION_DAYS = os.getenv("PRESIGNED_URL_EXPIRATION_DAYS")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")


def start_conversion(file: UploadFile) -> dict:
    """
    Uploads file to S3, and enqueues the Celery conversion task.
    Returns the task id.
    """

    s3_manager = S3Manager(
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_region=AWS_REGION,
        aws_s3_bucket_name=AWS_S3_BUCKET_NAME
    )

    filename, converted_filename = get_filenames(file.filename)
    s3_manager.upload_file_to_s3(file.file, filename)

    task = convert_file_and_upload__task.delay(filename, converted_filename)

    return {
        "task_id": task.id
    }


def get_conversion_status(task_id: str) -> dict:
    """
    Retrieves the result of a Celery conversion task.
    """

    task = AsyncResult(task_id)

    if task.ready():
        if task.successful():
            return {"status": "success", "converted_file_url": task.get()}
        else:
            task.forget()
            raise HTTPException(status_code=500, detail=str(task.result))

    return {"status": "pending", "message": "Task is still processing"}


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
