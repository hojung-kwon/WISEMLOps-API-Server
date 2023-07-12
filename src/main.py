import os
import logging
import sys
from contextlib import asynccontextmanager

from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from uvicorn import Config, Server
from loguru import logger
from fastapi import FastAPI, Request

from src.version import get_version_info, write_version_py
from src.exceptions import CustomHTTPError
from src.kubernetes_client.cluster import router as cluster_router
from src.kubernetes_client.crds import router as crd_router
from src.minio_client import router as minio_router
from src.mlflow_client import router as mlflow_router
from src.kserve_client import router as kserve_router
from src.kubernetes_client.kfp_client import router as kfp_router

LOG_LEVEL = logging.getLevelName(os.environ.get("LOG_LEVEL", "DEBUG"))
JSON_LOGS = True if os.environ.get("JSON_LOGS", "0") == "1" else False


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


def check_env_exist() -> None:
    """
    설정이 필요한 환경변수가 세팅되어있는지 체크
    TODO: 필요한 환경변수가 없을 경우, 프로그램 종료

    Returns: None

    """
    env_list = ['CHECK_ENV']  # TODO: 확인할 환경변수 설정
    for env in env_list:
        if env not in os.environ.keys():
            logging.warning(f"set {repr(env)} environment variable.")


@asynccontextmanager
async def lifespan(lifespan_app: FastAPI):
    # startup event
    logging.info("Start Python FastAPI Template")
    # logging.info("Check env exist ...")
    # check_env_exist()
    write_version_py()
    yield
    # shutdown event
    logging.info("Shut down Python FastAPI Template")


app = FastAPI(
    lifespan=lifespan,
    title="Python FastAPI Template",
    description="ML Ops Python FastAPI Template",
    version="0.0.1",
    # dependencies=[Depends(get_query_token)]
)

app.include_router(cluster_router.router)
app.include_router(crd_router.router)
app.include_router(minio_router.router)
app.include_router(mlflow_router.router)
app.include_router(kserve_router.router)
app.include_router(kfp_router.router)

origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


@app.get("/")
async def root():
    return {"title": app.title, "description": app.description, "version": app.version, "docs_url": app.docs_url}


@app.get("/health")
async def health():
    return {"status": "UP"}


@app.get("/info")
async def info():
    VERSION, GIT_REVISION, GIT_SHORT_REVISION, GIT_BRANCH, BUILD_DATE = get_version_info()
    return {
        "version": VERSION,
        "git_branch": GIT_BRANCH,
        "git_revision": GIT_REVISION,
        "git_short_revision": GIT_SHORT_REVISION,
        "build_date": BUILD_DATE
    }


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
