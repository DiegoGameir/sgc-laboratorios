from minio import Minio
from app.core.config import settings

# secure=False indica que usamos HTTP localmente. En producción (HTTPS) cambiará a True.
minio_client = Minio(
    settings.MINIO_HOST,
    access_key=settings.MINIO_USER,
    secret_key=settings.MINIO_PASSWORD,
    secure=False
)

def get_minio_client() -> Minio:
    return minio_client