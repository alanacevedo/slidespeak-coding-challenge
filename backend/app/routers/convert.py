from fastapi import APIRouter, UploadFile, HTTPException
from ..services.convert import start_conversion, get_conversion_status

router = APIRouter()

ALLOWED_CONTENT_TYPES = {
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".ppt": "application/vnd.ms-powerpoint"
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@router.post("/convert/", status_code=202)
async def convert(file: UploadFile):
    """
    Converts the powerpoint file to a pdf file with the unoserver API.
    Uploads both files to S3, and then generates and returns presigned url for the converted file.
    """

    filename_extension = '.' + file.filename.split('.')[-1] if '.' in file.filename else None

    if filename_extension not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Missing or invalid filename extension")

    if file.content_type != ALLOWED_CONTENT_TYPES[filename_extension]:
        raise HTTPException(status_code=400, detail="Uploaded file is not a PowerPoint file")

    contents = await file.read()

    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Uploaded file is too large")

    await file.seek(0)

    task_id_json = start_conversion(file)

    return task_id_json


@router.get("/convert/status/{task_id}")
async def conversion_status(task_id: str):
    """
    Checks the status of the conversion task and returns the result if available.
    """

    result = get_conversion_status(task_id)

    return result
