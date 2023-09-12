import json
from typing import Union

from kserve import ApiException
from mlflow import MlflowException


class KServeException(Exception):
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


MODULE_CODE = 703


class KServeApiError(KServeException):
    def __init__(self, e: Union[ApiException, MlflowException]):
        self.code = 400000
        self.message = 'BAD REQUEST'
        self.result = ['Your request has been denied.']

        if isinstance(e, ApiException):
            self.code = int(f"{MODULE_CODE}{e.status}")
            self.message = e.reason
            self.result = e.body
        elif isinstance(e, MlflowException):
            self.code = int(f"{MODULE_CODE}{e.error_code}")
            self.message = e.message
            self.result = e.json_kwargs
