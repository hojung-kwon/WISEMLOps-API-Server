from typing import Any

from pydantic import BaseModel
from starlette import status


class Response(BaseModel):
    """기본 API 응답 포맷 by AI플랫폼 Restful API 디자인 가이드"""
    code: int = 200000
    message: str = "API response success"
    result: Any

    @classmethod
    def from_result(cls, module_code, result):
        return cls(code=int(f"{module_code}{status.HTTP_200_OK}"), result=result)
