from minio import Minio

from core.config import get_settings

settings = get_settings()

# Initialize MinIO client
minio_client = Minio(
    settings.MINIO_HOST,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_SECURE
)


# Ensure default bucket exists
def init_minio():
    """Initialize MinIO by ensuring the default bucket exists"""
    try:
        if not minio_client.bucket_exists(settings.MINIO_BUCKET_NAME):
            minio_client.make_bucket(settings.MINIO_BUCKET_NAME)
    except Exception as e:
        print(f"Error creating bucket: {e}")
        raise
