from typing import List

from kserve import ApiException
from mlflow import MlflowException

from src.models import APIResponseModel


def response_error(e: object) -> APIResponseModel:
    code = 400000
    message = 'BAD REQUEST'
    result = ['Your request has been denied.']

    if isinstance(e, ApiException):
        code = int(str(e.status) + '000')
        message = e.reason
        result = e.body
    elif isinstance(e, MlflowException):
        code = int(str(e.get_http_status_code()) + '000')
        message = e.error_code
        result = e.message

    return APIResponseModel(code=code, message=message, result=result)


def response_success(result: object) -> APIResponseModel:
    if result is None:
        return APIResponseModel(result=['no content'])
    elif isinstance(result, List):
        return APIResponseModel(result=result)
    return APIResponseModel(result=[result])


def response(result: object) -> APIResponseModel:
    if isinstance(result, Exception):
        return response_error(result)
    elif isinstance(result, bool) and not result:
        return response_error(result)
    return response_success(result)
