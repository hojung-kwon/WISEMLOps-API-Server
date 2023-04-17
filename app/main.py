import os
import logging
import sys

from starlette.responses import JSONResponse
from uvicorn import Config, Server
from loguru import logger
from fastapi import Depends, FastAPI, Request

from dependencies import get_query_token, get_token_header
from exceptions import CustomHTTPError
from internal import admin
from routers import items, users

LOG_LEVEL = logging.getLevelName(os.environ.get("LOG_LEVEL", "DEBUG"))
JSON_LOGS = True if os.environ.get("JSON_LOGS", "0") == "1" else False


# sys.path.append('/path/to/dir')

class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging():
    # intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(LOG_LEVEL)

    # remove every other logger's handlers
    # and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # configure loguru
    logger.configure(handlers=[{"sink": sys.stdout, "serialize": JSON_LOGS}])


def check_env_exist() -> bool:
    """
    설정이 필요한 환경변수가 세팅되어있는지 체크
    TODO: 필요한 환경변수가 없을 경우, 프로그램 종료

    Returns: None

    """
    logging.info("Check env exist ...")
    env_list = []  # TODO: 확인할 환경변수 설정
    for env in env_list:
        if env not in os.environ.keys():
            logging.warning(f"set {repr(env)} environment variable.")
            return False
    return True


app = FastAPI(
    title="Python FastAPI Template",
    description="DE Team Python FastAPI Template",
    version="1.0.0",
    dependencies=[Depends(get_query_token)]
)

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,  # app/internal/admin.py 원본을 수정하지 않고 선언 가능
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.exception_handler(CustomHTTPError)
async def badrequest_handler(request: Request, exc: CustomHTTPError):
    return JSONResponse(status_code=400,
                        content={"code": exc.status_code, "message": f"{exc.detail}"})


@app.exception_handler(CustomHTTPError)
async def unauthorized_handler(request: Request, exc: CustomHTTPError):
    return JSONResponse(status_code=401,
                        content={"code": exc.status_code, "message": f"{exc.detail}"})


@app.exception_handler(CustomHTTPError)
async def forbidden_handler(request: Request, exc: CustomHTTPError):
    return JSONResponse(status_code=403,
                        content={"code": exc.status_code, "message": f"{exc.detail}"})


@app.exception_handler(CustomHTTPError)
async def notfound_handler(request: Request, exc: CustomHTTPError):
    return JSONResponse(status_code=404,
                        content={"code": exc.status_code, "message": f"{exc.detail}"})


@app.on_event("startup")
async def startup_event():
    logging.info("Start Python FastAPI Template")
    check_env_exist()


@app.get("/")
async def root():
    return {"title": app.title, "description": app.description, "version": app.version, "docs_url": app.docs_url}


@app.get("/health")
async def health():
    return {"status": "UP"}


if __name__ == "__main__":
    server = Server(
        Config(
            "main:app",
            host="0.0.0.0",
            port=8000,
            log_level=LOG_LEVEL,
        ),
    )

    # setup logging last, to make sure no library overwrites it
    # (they shouldn't, but it happens)
    setup_logging()
    # uvicorn.run(app=app, host="0.0.0.0", port=8000, log_level=LOG_LEVEL)
    server.run()
