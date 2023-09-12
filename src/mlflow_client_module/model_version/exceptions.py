import json
from ctypes import Union

from mlflow import MlflowException

from src.mlflow_client_module.model_version import MODULE_CODE


class MlflowVersionException(Exception):

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


class MlflowVersionError(MlflowVersionException):
    def __init__(self, e: Union[MlflowException]):
        body = json.loads(e.body)
        self.code = int(f"{MODULE_CODE}{e.status}")
        self.message = body['message']
        self.result = e.reason
