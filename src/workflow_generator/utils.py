import os
import string
import random

from typing import List

from src.models import APIResponseModel
from jinja2.exceptions import TemplateError


def get_workflow_name(name: str):
    if name is None or len(name.strip()) < 1:
        return make_workflow_name()
    return name


def make_workflow_name():
    source = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(source) for i in range(12)))
    return result_str


def get_workflow_generator_path():
    workflow_generator_path = os.path.join(os.getcwd(), "workflow_generator")
    return os.path.abspath(workflow_generator_path)


def response_error(e: TemplateError) -> APIResponseModel:
    code = 400000
    return APIResponseModel(code=code, message=e.message, result=e.args)


def response_success(result):
    if result is None:
        return APIResponseModel(result=['no content'])
    elif isinstance(result, List):
        return APIResponseModel(result=result)
    return APIResponseModel(result=[result])
