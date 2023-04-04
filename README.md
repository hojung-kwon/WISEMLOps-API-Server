# Python FastAPI Template

![PythonVersion](https://img.shields.io/badge/python-3.10-blue)
![FastAPIVersion](https://img.shields.io/badge/fastapi-0.95.0-yellowgreen)
![loguru](https://img.shields.io/badge/fastapi-0.6.0-orange)

DE팀 전용 FastAPI 개발 템플릿 


## Getting started

> API 명세는 와이즈넛 [Restful API 디자인 가이드](https://docs.google.com/document/d/1tSniwfrVaTIaTT4MxhBRAmv-S_ECcoSFAXlYrsg4K0Y/edit#heading=h.60fu2rc04bck)를 따른다.
- 해당 템플릿은 크게 **msa**와 **monlith** 두 가지로 나뉜다.
- Default는 **msa**(`$HOME/app`)로 해당 템플릿을 그대로 사용하면 된다.
- **monolith**를 사용할 경우, msa(`$HOME/app`, `$HOME/tests`)는 삭제하고 최상위 디렉터리인 monolith를 삭제한다.
> TODO: **monolith** 개발 (현재 디렉터리만 생성되어있어 사용 불가능) 

## MSA 구조
> @tiangolo(FastAPI 개발자)가 제공하는 유형(ex. api, crud, 모델, 스키마)별로 파일을 구분하는 프로젝트 구조
- 출처: https://fastapi.tiangolo.com/tutorial/bigger-applications/
```python
.
├── app                         # "app" is a Python package
│         ├── __init__.py       # this file makes "app" a "Python package"
│         ├── main.py           # "main" module, e.g. import app.main
│         ├── dependencies.py   # "dependencies" module, e.g. import app.dependencies
│         └── routers           # "routers" is a "Python subpackage"
│         │   ├── __init__.py   # makes "routers" a "Python subpackage"
│         │   ├── items.py      # "items" submodule, e.g. import app.routers.items
│         │   └── users.py      # "users" submodule, e.g. import app.routers.users
│         └── internal          # "internal" is a "Python subpackage"
│             ├── __init__.py   # makes "internal" a "Python subpackage"
│             └── admin.py      # "admin" submodule, e.g. import app.internal.admin
```

## Monolith
> @tiangolo 가 제공하는 유형(예: api, crud, 모델, 스키마)별로 파일을 구분하는 프로젝트 구조는 범위가 적은 마이크로 서비스 또는 프로젝트에 적합하지만 많은 도메인이 있는 모놀리식에는 맞출 수 없다.
> 더 확장 가능하고 진화할 수 있는 구조는 Netflix의 Dispatch 에서 영감을 얻었다.
- 출처: https://github.com/zhanymkanov/fastapi-best-practices
```python
fastapi-project
├── alembic/
├── src
│   ├── auth
│   │   ├── router.py
│   │   ├── schemas.py  # pydantic models
│   │   ├── models.py  # db models
│   │   ├── dependencies.py
│   │   ├── config.py  # local configs
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   ├── service.py
│   │   └── utils.py
│   ├── aws
│   │   ├── client.py  # client model for external service communication
│   │   ├── schemas.py
│   │   ├── config.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   └── utils.py
│   └── posts
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── models.py
│   │   ├── dependencies.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   ├── service.py
│   │   └── utils.py
│   ├── config.py  # global configs
│   ├── models.py  # global models
│   ├── exceptions.py  # global exceptions
│   ├── pagination.py  # global module e.g. pagination
│   ├── database.py  # db connection related stuff
│   └── main.py
├── tests/
│   ├── auth
│   ├── aws
│   └── posts
├── templates/
│   └── index.html
├── requirements
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── .env
├── .gitignore
├── logging.ini
└── alembic.ini
```
1. 모든 도메인 디렉토리를 `src`폴더 안에 저장
    1. `src/` - 가장 높은 수준의 앱, 공통 모델, 구성 및 상수 등을 포함합니다.
    2. `src/main.py` - FastAPI 앱을 초기화하는 프로젝트의 루트
2. 각 패키지에는 자체 라우터, 스키마, 모델 등이 있습니다.
    1. `router.pyh`  - 모든 끝점이 있는 각 모듈의 핵심입니다.
    2. `schemas.py`  - pydantic 모델의 경우
    3. `models.py` - db 모델의 경우
    4. `service.py` - 모듈별 비즈니스 로직
    5. `dependencies.py` - 라우터 종속성
    6. `constants.py` - 모듈별 상수 및 오류 코드
    7. `config.py` - 예를 들어 환경 변수
    8. `utils.py` - 비업무 논리 기능, 예: 응답 정규화, 데이터 보강 등
    9. `exceptionsPostNotFoundInvalidUserData` - 모듈별 예외, 예: `PostNotFound`,`InvalidUserData`


## TODO
- [ ] API token을 JWT token으로 설정
- [ ] filtering, sorting, searching 기능을 query string으로 적용하기
- [ ] 버전 관리 (버전별 URL 표기)
- [ ] 링크 처리시 HATEOS를 이용한 링크 처리
- [ ] 에러 처리