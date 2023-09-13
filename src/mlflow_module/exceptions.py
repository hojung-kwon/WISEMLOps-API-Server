import json

from mlflow import MlflowException as MlflowApiException

from src.mlflow_module.config import MODULE_CODE


class MlflowException(Exception):

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


class MlflowApiError(MlflowException):
    def __init__(self, e: MlflowApiException):
        self.code = int(f"{MODULE_CODE}{e.error_code}")
        self.message = e.message
        self.result = e.json_kwargs
