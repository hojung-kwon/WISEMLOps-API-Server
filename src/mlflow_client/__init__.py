import os

from mlflow.tracking import MlflowClient

from src import app_config

os.environ["MLFLOW_S3_ENDPOINT_URL"] = app_config.MINIO_ENDPOINT
os.environ["AWS_ACCESS_KEY_ID"] = app_config.MINIO_ACCESS_KEY
os.environ["AWS_SECRET_ACCESS_KEY"] = app_config.MINIO_SECRET_KEY
os.environ["MLFLOW_TRACKING_URI"] = app_config.MLFLOW_TRACKING_URI

_mlflow_client = MlflowClient()
