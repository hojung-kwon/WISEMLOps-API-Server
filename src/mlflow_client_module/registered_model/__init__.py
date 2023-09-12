import os

from src import app_config
from src.mlflow_client_module.registered_model.service import RegisteredModelService

os.environ["MLFLOW_S3_ENDPOINT_URL"] = app_config.MINIO_ENDPOINT
os.environ["AWS_ACCESS_KEY_ID"] = app_config.MINIO_ACCESS_KEY
os.environ["AWS_SECRET_ACCESS_KEY"] = app_config.MINIO_SECRET_KEY
os.environ["MLFLOW_TRACKING_URI"] = app_config.MLFLOW_TRACKING_URI

MODULE_CODE = 603

service = RegisteredModelService()
