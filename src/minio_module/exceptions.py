import json

from minio.error import MinioException


class MinIOException(Exception):
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


MODULE_CODE = 704


class MinIOApiError(MinIOException):
    def __init__(self, e: MinioException):
        self.code = int(f"{MODULE_CODE}400")
        self.message = "minioException"
        self.result = e.args
