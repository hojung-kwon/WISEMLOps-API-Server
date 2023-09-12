from src import app_config


def get_kube_config_path():
    return app_config.CLUSTER_KUBE_CONFIG_PATH


def get_mlflow_s3_endpoint_url():
    return app_config.MINIO_ENDPOINT


def get_aws_access_key_id():
    return app_config.MINIO_ACCESS_KEY


def get_aws_secret_access_key():
    return app_config.MINIO_SECRET_KEY


def get_mlflow_tracking_uri():
    return app_config.MLFLOW_TRACKING_URI
