from typing import List

from minio.error import MinioException

from src.models import APIResponseModel


def response_error(e: MinioException) -> APIResponseModel:
    code = int(str(e.response.status) + '000')
    return APIResponseModel(code=code, message=e.response.reason, result=e.args)


def response_success(result):
    if result is None:
        return APIResponseModel(result=['no content'])
    elif isinstance(result, List):
        return APIResponseModel(result=result)
    return APIResponseModel(result=[result])
