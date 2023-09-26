import os.path
from typing import Dict, Optional

from jinja2 import Template, TemplateError

from src.workflow_generator_module.exceptions import WorkflowTemplateError
from src.workflow_generator_module.schemas import PipelineInfo, DagInfo, Pipeline
from src.workflow_generator_module.utils import get_workflow_name, get_workflow_generator_path


class PipelineGenService:
    def __init__(self, kfp_template: Template, airflow_template: Template, env_variables: Dict):
        self.kfp_template = kfp_template
        self.airflow_template = airflow_template
        self.env_variables = env_variables

    def _get_rendered_kfp_pipeline_dsl(self, pipeline_info: PipelineInfo, yaml_file: Optional[str] = None):
        pipeline_dsl = self.kfp_template.render(
            pipeline_info=pipeline_info,
            yaml_file=yaml_file,
        )
        return pipeline_dsl

    def _write_kfp_pipeline_dsl_file(self, pipeline_info: PipelineInfo, output_path: Optional[str] = None):
        pipeline_info.pipeline_name = get_workflow_name(pipeline_info.pipeline_name)
        dsl_file = os.path.join(output_path, f"{pipeline_info.pipeline_name}.py")
        yaml_file_path = os.path.abspath(os.path.join(output_path, f"{pipeline_info.pipeline_name}.yaml"))
        yaml_file = "/".join(yaml_file_path.split(os.sep))
        pipeline_dsl = self._get_rendered_kfp_pipeline_dsl(pipeline_info=pipeline_info,
                                                           yaml_file=yaml_file)
        with open(dsl_file, "w", encoding='utf-8') as dsl_output:
            dsl_output.write(pipeline_dsl)
        return dsl_file, yaml_file_path

    def make_kfp_pipeline_yaml(self, pipeline_info: PipelineInfo):
        try:
            output_path = os.path.join(get_workflow_generator_path(), "output")
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            dsl_file, yaml_file_path = self._write_kfp_pipeline_dsl_file(pipeline_info, output_path=output_path)
            os.system("python " + dsl_file)
            if os.path.exists(yaml_file_path):
                return Pipeline(pipeline_name=pipeline_info.pipeline_name,
                                pipeline_package_path=yaml_file_path,
                                description=pipeline_info.pipeline_description)
            return None
        except TemplateError as te:
            raise WorkflowTemplateError(te)

    def _get_rendered_airflow_dag(self, dag_info: DagInfo, pipeline_info: PipelineInfo):
        workflow = self.airflow_template.render(
            dag_info=dag_info,
            pipeline_info=pipeline_info,
        )
        return workflow

    def make_airflow_dag_file(self, dag_info: DagInfo, pipeline_info: PipelineInfo):
        try:
            output_path = os.path.join(get_workflow_generator_path(), "output")
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            dag_file = os.path.join(output_path, f"{dag_info.dag_id}.py")
            dag = self._get_rendered_airflow_dag(dag_info, pipeline_info)
            with open(dag_file, "w") as dag_output:
                dag_output.write(dag)
            return dag_info
        except TemplateError as te:
            raise WorkflowTemplateError(te)
