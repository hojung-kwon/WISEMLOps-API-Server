from src import app_config

MINIO_ENDPOINT = app_config.MINIO_ENDPOINT.split("://")[-1]
MINIO_ACCESS_KEY = app_config.MINIO_ACCESS_KEY
MINIO_SECRET_KEY = app_config.MINIO_SECRET_KEY
MINIO_SECURE = True if app_config.MINIO_ENDPOINT.split("://")[0] == "https" else False
