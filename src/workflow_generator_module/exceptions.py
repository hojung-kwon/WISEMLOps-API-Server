import json

from jinja2 import TemplateError
from starlette import status

from src.workflow_generator_module.config import MODULE_CODE


class WorkflowGeneratorException(Exception):
    def __init__(self, code: int, message: str, result):
        self.code = code
        self.message = message
        self.result = result

    def __str__(self):
        exception_data = {
            "code": self.code,
            "message": self.message,
            "result": self.result
        }
        return json.dumps(exception_data, indent=4, ensure_ascii=False)


class WorkflowTemplateError(WorkflowGeneratorException):
    def __init__(self, template_error: TemplateError):
        self.code = int(f"{MODULE_CODE}{status.HTTP_400_BAD_REQUEST}")
        self.message = template_error.message
        self.result = template_error.args
