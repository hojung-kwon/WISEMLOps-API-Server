import json

from kubernetes.client import ApiException


class KubernetesException(Exception):
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


MODULE_CODE = 702


class KubernetesApiError(KubernetesException):
    def __init__(self, e: ApiException):
        body = json.loads(e.body)
        self.code = int(f"{MODULE_CODE}{e.status}")
        self.message = e.reason
        self.result = body['message']
