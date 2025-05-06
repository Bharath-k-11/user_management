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
        "MINIO_ENDPOINT": "localhost:9000",
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

def test_upload_profile_picture_success(mock_minio_client, mock_settings):
    file_data = io.BytesIO(b"mock file content")
    file_name = "profile-picture.jpg"
    bucket_name = mock_settings["MINIO_BUCKET_NAME"]

    mock_minio_client.put_object.return_value = None
    result_url = upload_profile_picture(file_data, file_name)

    mock_minio_client.put_object.assert_called_once_with(
        bucket_name, file_name, file_data, length=-1, part_size=10 * 1024 * 1024
    )
    expected_url = f"{mock_settings['MINIO_ENDPOINT']}/{bucket_name}/{file_name}"
    assert result_url == expected_url

def test_get_profile_picture_url_success(mock_minio_client, mock_settings):
    file_name = "profile-picture.jpg"
    bucket_name = mock_settings["MINIO_BUCKET_NAME"]
    expected_presigned_url = "http://localhost:9000/test-bucket/profile-picture.jpg"

    mock_minio_client.get_presigned_url.return_value = expected_presigned_url
    result_url = get_profile_picture_url(file_name)

    mock_minio_client.get_presigned_url.assert_called_once_with(
        "GET", bucket_name, file_name
    )
    assert result_url == expected_presigned_url

def test_get_profile_picture_url_non_existent_file(mock_minio_client):
    file_name = "non-existent.jpg"
    mock_minio_client.get_presigned_url.side_effect = Exception("File not found")

    with pytest.raises(Exception, match="File not found"):
        get_profile_picture_url(file_name)


def test_upload_profile_picture_large_file(mock_minio_client, mock_settings):
    file_data = io.BytesIO(b"0" * (20 * 1024 * 1024))  # 20 MB file
    file_name = "large-profile-picture.jpg"
    bucket_name = mock_settings["MINIO_BUCKET_NAME"]

    mock_minio_client.put_object.return_value = None
    result_url = upload_profile_picture(file_data, file_name)

    mock_minio_client.put_object.assert_called_once_with(
        bucket_name, file_name, file_data, length=-1, part_size=10 * 1024 * 1024
    )
    expected_url = f"{mock_settings['MINIO_ENDPOINT']}/{bucket_name}/{file_name}"
    assert result_url == expected_url


def test_get_profile_picture_url_invalid_bucket(mock_minio_client):
    file_name = "profile-picture.jpg"
    mock_minio_client.get_presigned_url.side_effect = Exception("Bucket not found")

    with pytest.raises(Exception, match="Bucket not found"):
        get_profile_picture_url(file_name)


def test_upload_profile_picture_special_characters(mock_minio_client, mock_settings):
    file_data = io.BytesIO(b"mock file content")
    file_name = "profile@picture#$.jpg"
    bucket_name = mock_settings["MINIO_BUCKET_NAME"]

    mock_minio_client.put_object.return_value = None
    result_url = upload_profile_picture(file_data, file_name)

    mock_minio_client.put_object.assert_called_once_with(
        bucket_name, file_name, file_data, length=-1, part_size=10 * 1024 * 1024
    )
    expected_url = f"{mock_settings['MINIO_ENDPOINT']}/{bucket_name}/{file_name}"
    assert result_url == expected_url
