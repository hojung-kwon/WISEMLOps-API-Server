from typing import List

from fastapi import HTTPException

from src.models import APIResponseModel


def response_error(e: HTTPException) -> APIResponseModel:
    code = int(str(e.get_http_status_code()) + '000')
    return APIResponseModel(code=code, message=e.error_code, result=e.message)


def response_success(result):
    if result is None:
        return APIResponseModel(result=['no content'])
    elif isinstance(result, List):
        return APIResponseModel(result=result)
    return APIResponseModel(result=[result])
