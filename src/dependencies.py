"""
- 예제 단순화를 위한 커스텀 헤더를 사용한다.
- 실제로는 보안, 인증 및 권한 부여를 처리하기 위한 apiKey, http, oauth2, openIdConnect 등의
  통합된 [Security utilites](https://fastapi.tiangolo.com/tutorial/security/)를 사용해야 한다.
- TODO: JWT token 사용하여 공통 인증 서비스 연동
"""

from typing import Annotated

from fastapi import Header
from starlette import status

from src.exceptions import CustomHTTPError

DEFAULT_X_TOKEN = "fake-super-secret-token"
DEFAULT_TOKEN = "default-token"


async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != DEFAULT_X_TOKEN:
        raise CustomHTTPError(status_code=status.HTTP_400_BAD_REQUEST, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != DEFAULT_TOKEN:
        raise CustomHTTPError(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token provided")