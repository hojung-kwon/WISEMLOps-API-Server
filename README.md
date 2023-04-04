# Python FastAPI Template

![PythonVersion](https://img.shields.io/badge/python-3.10-blue)
![FastAPIVersion](https://img.shields.io/badge/fastapi-0.95.0-yellowgreen)
![loguru](https://img.shields.io/badge/loguru-0.6.0-orange)

DE팀 전용 FastAPI 개발 템플릿 


## Getting started

> API 명세는 와이즈넛 [Restful API 디자인 가이드](https://docs.google.com/document/d/1tSniwfrVaTIaTT4MxhBRAmv-S_ECcoSFAXlYrsg4K0Y/edit#heading=h.60fu2rc04bck)를 따른다.
- 해당 템플릿은 크게 **msa**와 **monlith** 두 가지로 나뉜다.
- Default는 **msa**(`$HOME/app`)로 해당 템플릿을 그대로 사용하면 된다.
- **monolith**를 사용할 경우, msa (`$HOME/app`, `$HOME/tests`)는 삭제하고 최상위 디렉터리인 monolith를 삭제한다.
- 🔨 **TODO**: **monolith** 개발 (현재 디렉터리만 생성되어있어 사용 불가능) 

## MSA
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


## 🚀 TODO
- [ ] DB 적용한 API 동작 테스트
- [ ] API token을 JWT token으로 설정
- [ ] filtering, sorting, searching 기능을 query string으로 적용하기
- [ ] 버전 관리 (버전별 URL 표기)
- [ ] 링크 처리시 HATEOS를 이용한 링크 처리
- [ ] 에러 처리