from typing import List

from fastapi import HTTPException

from src.models import APIResponseModel


def response_error(e: HTTPException) -> APIResponseModel:
    code = int(str(e.status_code) + '000')
    return APIResponseModel(code=code, message=e.detail, result=e.args)


def response_success(result):
    if result is None:
        return APIResponseModel(result=[])
    elif isinstance(result, List):
        return APIResponseModel(result=result)
    return APIResponseModel(result=[result])
