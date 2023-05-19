from typing import Any

from pydantic import BaseModel


class Tag(BaseModel):
    key: str
    value: Any = None
