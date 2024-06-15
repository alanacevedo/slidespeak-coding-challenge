import pytest
from fastapi.testclient import TestClient
from moto import mock_aws
import os
from app.main import app
from app.utils.s3_utils import S3Manager

# Set environment variables for testing
os.environ["AWS_ACCESS_KEY"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
os.environ["AWS_S3_BUCKET_NAME"] = "test-bucket"
os.environ["AWS_REGION"] = "us-east-1"
os.environ["PRESIGNED_URL_EXPIRATION_DAYS"] = "5"

client = TestClient(app)


@pytest.fixture
def s3_manager():
    with mock_aws():
        manager = S3Manager(
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            aws_region=os.getenv(os.getenv("AWS_REGION")),
            aws_s3_bucket_name=os.getenv("AWS_S3_BUCKET_NAME")
        )
        manager.s3_client.create_bucket(Bucket=os.getenv("AWS_S3_BUCKET_NAME"))
        yield manager


def test_initialize_client(s3_manager: S3Manager):
    assert s3_manager is not None and s3_manager.s3_client is not None


def test_upload_file_to_s3(s3_manager: S3Manager):
    test_filename = "Test_PPTX.pptx"
    test_file_path = "tests/test_files/" + test_filename
    with open(test_file_path, "rb") as test_file:
        s3_manager.upload_file_to_s3(test_file, test_filename)
    # check if file was uploaded to mock s3
    file_exists = s3_manager.s3_client.head_object(Bucket=s3_manager.bucket_name, Key=test_filename)
    assert file_exists


def test_generate_presigned_url(s3_manager: S3Manager):
    test_filename = "Test_PPTX.pptx"
    test_file_path = "tests/test_files/" + test_filename
    with open(test_file_path, "rb") as test_file:
        s3_manager.upload_file_to_s3(test_file, test_filename)

    file_url = s3_manager.generate_presigned_url(test_filename, os.getenv("PRESIGNED_URL_EXPIRATION_DAYS"))

    assert isinstance(file_url, str) and len(file_url) > 0
