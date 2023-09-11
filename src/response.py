from typing import List

from src.models import APIResponseModel


class Response(APIResponseModel):
    @classmethod
    def from_result(cls, result):
        if result is None:
            return cls(result=[])
        elif isinstance(result, List):
            return cls(result=result)
        return cls(result=[result])
