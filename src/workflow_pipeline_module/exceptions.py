import json

from starlette import status

from src.workflow_pipeline_module.config import MODULE_CODE


class WorkflowPipelineException(Exception):
    """파이프라인 생성 서비스에서 발생할 수 있는 예외처리 포맷"""

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


class PipelineNotFoundError(WorkflowPipelineException):
    """파이프라인 미존재"""

    def __init__(self, pipeline):
        self.code = int(f"{MODULE_CODE}{status.HTTP_404_NOT_FOUND}")
        self.message = "Pipeline Not Found"
        self.result = {"current_pipeline": pipeline}


class PipelineAlreadyExistsError(WorkflowPipelineException):
    """파이프라인 미존재"""

    def __init__(self, pipeline):
        self.code = int(f"{MODULE_CODE}{status.HTTP_409_CONFLICT}")
        self.message = "Pipeline already exists"
        self.result = {"current_pipeline": pipeline}


class PipelineCreateError(WorkflowPipelineException):
    """파이프라인 저장 에러"""

    def __init__(self, pipeline, message):
        self.code = int(f"{MODULE_CODE}{status.HTTP_500_INTERNAL_SERVER_ERROR}")
        self.message = f"CreatePipeline failed : {message}"
        self.result = {"current_pipeline": pipeline}
