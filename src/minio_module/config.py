from src import app_config

MODULE_CODE = 104


def get_minio_endpoint():
    return app_config.MINIO_ENDPOINT


def get_minio_access_key():
    return app_config.MINIO_ACCESS_KEY


def get_minio_secret_key():
    return app_config.MINIO_SECRET_KEY