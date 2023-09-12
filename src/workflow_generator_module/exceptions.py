import json

from jinja2 import TemplateError


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
        self.code = 400000
        self.message = template_error.message
        self.result = template_error.args
