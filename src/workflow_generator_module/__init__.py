from src.workflow_generator_module.config import get_template, get_mlflow_s3_endpoint_url, get_mlflow_tracking_uri, \
    get_aws_access_key_id, get_aws_secret_access_key
from src.workflow_generator_module.service import PipelineGenService

pipeline_gen_service = PipelineGenService(
    kfp_template=get_template("kfp"),
    airflow_template=get_template("airflow"),
    mlflow_s3_endpoint_url=get_mlflow_s3_endpoint_url(),
    mlflow_tracking_uri=get_mlflow_tracking_uri(),
    aws_access_key_id=get_aws_access_key_id(),
    aws_secret_access_key=get_aws_secret_access_key()
)
