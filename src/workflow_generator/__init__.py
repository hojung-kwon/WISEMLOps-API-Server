from src.workflow_generator.config import get_template, get_env_variables
from src.workflow_generator.service import PipelineGenService

pipeline_gen_service = PipelineGenService(
    kfp_template=get_template("kfp"),
    airflow_template=get_template("airflow"),
    env_variables=get_env_variables(),
)
