import os

from src.kserve_module.config import get_mlflow_s3_endpoint_url, get_aws_access_key_id, get_aws_secret_access_key, \
    get_mlflow_tracking_uri, get_kube_config_path
from src.kserve_module.service import KServeService

os.environ["MLFLOW_S3_ENDPOINT_URL"] = get_mlflow_s3_endpoint_url()
os.environ["AWS_ACCESS_KEY_ID"] = get_aws_access_key_id()
os.environ["AWS_SECRET_ACCESS_KEY"] = get_aws_secret_access_key()
os.environ["MLFLOW_TRACKING_URI"] = get_mlflow_tracking_uri()

service = KServeService(config_file=get_kube_config_path())
