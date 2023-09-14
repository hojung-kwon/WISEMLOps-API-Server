from starlette import status

from src import app_config


class MLOpsAPIException(Exception):
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
        import json
        return json.dumps(exception_data, indent=4, ensure_ascii=False)


class TokenValidationError(MLOpsAPIException):
    def __init__(self, x_token):
        self.code = int(f"{app_config.SERVICE_CODE}{status.HTTP_401_UNAUTHORIZED}")
        self.message = "Invalid x-token header"
        self.result = {"current_x_token": x_token}


class TokenProvisionError(MLOpsAPIException):
    def __init__(self, x_token):
        self.code = int(f"{app_config.SERVICE_CODE}{status.HTTP_401_UNAUTHORIZED}")
        self.message = "Invalid token provided"
        self.result = {"current_x_token": x_token}
