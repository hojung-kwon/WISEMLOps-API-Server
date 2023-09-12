import json
from typing import Union

from kfp_server_api import ApiException as KFPApiException
from kubernetes.client import ApiException as KubernetesApiException

from src.kfp_module.config import MODULE_CODE


class KFPException(Exception):
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


class KFPApiError(KFPException):
    def __init__(self, e: Union[KFPApiException, KubernetesApiException]):
        body = json.loads(e.body)
        self.code = int(f"{MODULE_CODE}{e.status}")
        self.message = e.reason
        self.result = body['message']
