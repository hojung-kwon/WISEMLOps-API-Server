"""
users API는 간단한 예시로 실제 개발시 items API를 참고하길 바람
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.models import APIResponseModel

router = APIRouter()    # APIRouter 변수명은 원하는대로 설정 가능

fake_users_db = [{"username": "Rick"}, {"username": "Morty"}]

@router.get("/users", tags=["users"], response_model=APIResponseModel, response_class=JSONResponse)
async def read_users():
    return {"result": fake_users_db}


@router.get("/users/me", tags=["users"], response_model=APIResponseModel, response_class=JSONResponse)
async def read_user_me():
    return {"result": {"username": "fakecurrentuser"}}


@router.get("/users/{username}", tags=["users"], response_model=APIResponseModel, response_class=JSONResponse)
async def read_user(username: str):
    return {"result": {"username": username}}