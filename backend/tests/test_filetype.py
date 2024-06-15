from fastapi.testclient import TestClient

from app.main import app

test_client = TestClient(app)


def test_convert_invalid_filetype():
    with open("tests/test_files/Test_TXT.txt", "rb") as file:
        response = test_client.post(
            "/convert/",
            files={"file": ("Test_TXT.txt", file, "text/plain")}
        )

    assert response.status_code == 400
    assert response.json() == {"detail": "Missing or invalid filename extension"}
