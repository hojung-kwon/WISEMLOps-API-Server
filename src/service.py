from jinja2 import TemplateError
from kfp_server_api import ApiException as KFPApiException
from kubernetes.client import ApiException as KubernetesApiException

from src.kfp_module import kfp_service
from src.kfp_module.exceptions import KFPApiError
from src.workflow_generator_module import pipeline_gen_service
from src.workflow_generator_module.exceptions import WorkflowTemplateError
from src.workflow_generator_module.schemas import PipelineInfo
from src.workflow_pipeline_module import get_db, workflow_pipeline_service
from src.workflow_pipeline_module.exceptions import PipelineCreateError
from src.workflow_pipeline_module.schemas import Pipeline


class WorkflowPipelineService:
    def __init__(self):
        pass

    def make_pipeline(self, pipeline_info: PipelineInfo):
        try:
            # workflow/kfp 호출, pipeline tar.gz 생성
            pipeline = pipeline_gen_service.make_kfp_pipeline_tar_gz(pipeline_info)

            if pipeline is None:
                pass
        except TemplateError as te:
            raise WorkflowTemplateError(te)

        try:
            # pipeline upload
            result = kfp_service.upload_pipeline(pipeline)
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

        try:
            # db save
            pipeline_id = str(result.id)
            pipeline_name = result.name
            pipeline_description = result.description
            version_info = result.default_version
            nodes = pipeline_info.nodes
            edges = pipeline_info.edges
            position = pipeline_info.position
            zoom = pipeline_info.zoom

            db_pipeline = Pipeline(pipeline_id,
                                   pipeline_name,
                                   pipeline_description,
                                   version_info,
                                   nodes,
                                   edges,
                                   position,
                                   zoom)

            result = workflow_pipeline_service.create_pipeline(db=get_db, pipeline=db_pipeline)
        except PipelineCreateError as pe:
            raise PipelineCreateError(pipeline, pe.message)
        return result
