from src import app_config
from src.minio_module.service import MinIOService

MINIO_ENDPOINT = app_config.MINIO_ENDPOINT
MINIO_ACCESS_KEY = app_config.MINIO_ACCESS_KEY
MINIO_SECRET_KEY = app_config.MINIO_SECRET_KEY

service = MinIOService(endpoint=MINIO_ENDPOINT, access_key=MINIO_ACCESS_KEY, secret_key=MINIO_SECRET_KEY)