from minio import Minio
from minio.error import S3Error
from app.dependencies import get_settings

settings = get_settings()

minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_USE_SSL
)


def ensure_minio_bucket(bucket_name: str):
    """Ensure that the specified bucket exists in MinIO."""
    try:
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
    except S3Error as e:
        print(f"MinIO bucket error: {e}")


def upload_profile_picture(file_data, file_name: str) -> str:
    if not file_name.lower().endswith((".jpg", ".jpeg", ".png")):
        raise ValueError("Unsupported file type")

    bucket_name = settings.MINIO_BUCKET_NAME

    minio_client.put_object(
        bucket_name, file_name, file_data, length=-1, part_size=10 * 1024 * 1024
    )

    return f"{settings.MINIO_ENDPOINT}/{bucket_name}/{file_name}"


def get_profile_picture_url(file_name: str) -> str:
    bucket_name = settings.MINIO_BUCKET_NAME
    try:
        return minio_client.get_presigned_url("GET", bucket_name, file_name)
    except Exception as e:
        raise e

