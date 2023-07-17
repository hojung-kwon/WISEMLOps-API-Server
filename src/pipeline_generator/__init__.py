from src.pipeline_generator.config import get_template, get_env_variables
from src.pipeline_generator.service import PipelineGenService

pipeline_gen_service = PipelineGenService(
    template=get_template(),
    env_variables=get_env_variables(),
)
