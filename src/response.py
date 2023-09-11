from typing import List, Any

from pydantic import BaseModel


class Response(BaseModel):
    """기본 API 응답 포맷 by AI플랫폼 Restful API 디자인 가이드"""
    code: int = 200000
    message: str = "API response success"
    result: Any

    @classmethod
    def from_result(cls, result):
        if result is None:
            return cls(result=[])
        elif isinstance(result, List):
            return cls(result=result)
        return cls(result=[result])
