import os.path
from typing import Dict, Optional

from jinja2 import Template, TemplateError

from src.pipeline_generator.models import PipelineInfo
from src.pipeline_generator.utils import get_pipeline_name, response_error, response_success, \
    get_pipeline_generator_path


class PipelineGenService:
    def __init__(self, template: Template, env_variables: Dict):
        self.template = template
        self.env_variables = env_variables

    def _get_rendered_pipeline_dsl(self, pipeline_info: PipelineInfo, tar_file: Optional[str] = None):
        pipeline_dsl = self.template.render(
            pipeline_name=pipeline_info.pipeline_name,
            pipeline_description=pipeline_info.pipeline_description,
            env_variables=self.env_variables,
            pipeline_info=pipeline_info,
            tar_file=tar_file,
        )
        return pipeline_dsl

    def _write_pipeline_dsl_file(self, pipeline_info: PipelineInfo, output_path: Optional[str] = None):
        pipeline_info.pipeline_name = get_pipeline_name(pipeline_info.pipeline_name)
        dsl_file = os.path.join(output_path, f"{pipeline_info.pipeline_name}.py")
        tar_file = os.path.join(output_path, f"{pipeline_info.pipeline_name}.tar.gz")
        pipeline_dsl = self._get_rendered_pipeline_dsl(pipeline_info, tar_file)
        with open(dsl_file, "w") as dsl_output:
            dsl_output.write(pipeline_dsl)
        return dsl_file

    def make_pipeline_tar_gz(self, pipeline_info: PipelineInfo):
        try:
            output_path = os.path.join(get_pipeline_generator_path(), "output")
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            dsl_file = self._write_pipeline_dsl_file(pipeline_info, output_path=output_path)
            os.system("python " + dsl_file)
        except TemplateError as te:
            return response_error(te)
        return response_success(pipeline_info)
