import os
import string
import random

from typing import List

from src.models import APIResponseModel
from jinja2.exceptions import TemplateError


def get_pipeline_name(name: str):
    if name is None or len(name.strip()) < 1:
        return make_pipeline_name()
    return name


def make_pipeline_name():
    source = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(source) for i in range(12)))
    return result_str


def get_pipeline_generator_path():
    pipeline_generator_path = os.path.join(os.getcwd(), "pipeline_generator")
    return os.path.abspath(pipeline_generator_path)


def response_error(e: TemplateError) -> APIResponseModel:
    code = 400000
    return APIResponseModel(code=code, message=e.message, result=e.args)


def response_success(result):
    if result is None:
        return APIResponseModel(result=['no content'])
    elif isinstance(result, List):
        return APIResponseModel(result=result)
    return APIResponseModel(result=[result])
