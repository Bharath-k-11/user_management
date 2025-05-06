import io
import pytest
from unittest.mock import patch
from app.utils.minio_client import upload_profile_picture, get_profile_picture_url


@pytest.fixture
def mock_minio_client():
    """Fixture to mock the Minio client."""
    with patch("app.utils.minio_client.minio_client", autospec=True) as mock_client:
        yield mock_client


@pytest.fixture
def mock_settings():
    """Fixture to mock the settings."""
    return {
        "MINIO_ENDPOINT": "minio:9000",
        "MINIO_BUCKET_NAME": "bucket_name",
        "MINIO_ACCESS_KEY": "test-access-key",
        "MINIO_SECRET_KEY": "test-secret-key",
        "MINIO_BUCKET_NAME" : "demo",
        "MINIO_USE_SSL": False,
    }

def test_upload_profile_picture_invalid_file_type(mock_minio_client):
    file_data = io.BytesIO(b"mock file content")
    file_name = "profile-picture.txt"  # Invalid file type

    with pytest.raises(ValueError, match="Unsupported file type"):
        upload_profile_picture(file_data, file_name)
