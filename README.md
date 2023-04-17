# Python FastAPI Template

![PythonVersion](https://img.shields.io/badge/python-3.10-blue)
![FastAPIVersion](https://img.shields.io/badge/fastapi-0.95.0-yellowgreen)
![loguru](https://img.shields.io/badge/loguru-0.6.0-orange)

### DE팀 전용 FastAPI 개발 템플릿 

> API 명세는 와이즈넛 [Restful API 디자인 가이드](https://docs.google.com/document/d/1tSniwfrVaTIaTT4MxhBRAmv-S_ECcoSFAXlYrsg4K0Y/edit#heading=h.60fu2rc04bck)를 따른다.


## Getting started

### 1. Create Project
1. GitLab **Create new project** 을 통해 새로운 프로젝트 생성
2. **Create from template** 선택
3. **Group** 선택
4. **wisenut/DE/테스트베드:Python FastAPI Template** 에서 **Use template** 선택
5. _Project name, Project description (optional)_ 등을 작성하고 **Create project** 선택
6. 🔴 **gitlab-ci Container Registry Deploy**를 위해 프로젝트 생성시 무조건 `Settings > Repository > Deploy tokens`에 **Name: gitlab+deploy-token** 으로 토큰 생성하기 🔴

### 2. Development Environment Setting
1. 로컬 개발 환경에 `git clone ...` 
2. Pycharm 을 열고 `open project ...`
3. **Poetry** Setting (OR **venv** 사용)
   1. Poetry 설치 ([poetry docs](https://python-poetry.org/docs/#installation) 참고)
   2. **Add New Interpreter** 선택
   3. **Add Local Interpreter** 선택
   4. **Poetry Environment** 선택
   5. Python version에 맞게 환경 설정 (현재는 3.10 사용중)
   6. **Install packages from pyproject.toml** 체크
      - `UnicodeError` 발생 할 경우, **Settings > Editor > Global Encoding, Project Encoding, Properties Files** 모두 'UTF-8' 로 설정
      - 🐛 해결이 안 될 경우, 체크 표시 해제하고 poetry 가상환경 생성한 후 poetry venv 터미널에 `poetry install`로 직접 Installs the project dependencies
   7. **OK** 선택
4. 로컬 구동 (`$HOME/main.py`) or `docker build ...` && `docker run -d -p ...` 로 컨테이너 빌드 & 구동
5. `http :8000/openapi.json` or _http://localhost:8000/docs_ 로 API 명세 확인 및 테스트

### 📚 참고 사항 📚   
- 해당 템플릿은 크게 **msa**와 **monlith** 두 가지로 나뉜다.
- Default는 **msa**(`$HOME/app`)로 해당 템플릿을 그대로 사용하면 된다.
- **monolith**를 사용할 경우, msa (`$HOME/app`, `$HOME/tests`)는 삭제하고 최상위 디렉터리인 monolith를 삭제 후 사용한다.
- DB를 사용하지 않을 경우, 관련된 코드는 모두 삭제한다. (`crud.py`, `database.py`, `schemas.py` 등)


## MSA
> @tiangolo(FastAPI 개발자)가 제공하는 유형(ex. api, crud, 모델, 스키마)별로 파일을 구분하는 프로젝트 구조
- 출처: https://fastapi.tiangolo.com/tutorial/bigger-applications/
```python
.
├── app                  # "app" is a Python package
│   ├── __init__.py      # 
│   ├── main.py          # 
│   ├── dependencies.py  # 
│   ├── exceptions.py  # custom exception
│   ├── models.py  # 
│   ├── schemas.py  # 데이터베이스를 사용할 경우
│   ├── database.py  # 데이터베이스를 사용할 경우
│   ├── crud.py  # 데이터베이스를 사용할 경우
│   └── routers          # (API Endpoints) "routers" is a "Python subpackage" 
│   │   ├── __init__.py  # 
│   │   ├── items.py     # 
│   │   └── users.py     # 
│   └── internal         # 
│       ├── __init__.py  # 
│       └── admin.py     # 
│   └── src         # (Main Functions) "src" is a "Python subpackage"
│       ├── __init__.py  # 
├── tests                  # app directory architecture 에 맞게 unit test 구성
│   ├── __init__.py      # 
│   └── routers          # 
│   │   ├── __init__.py  # 
│   │   ├── test_items.py     # 
│   │   └── test_users.py     # 
│   └── internal         # 
│       ├── __init__.py  # 
│       └── test_admin.py     # 
│   └── src         # 
│       ├── __init__.py  #
```

- **routers**: API Endpoint. 작성한 API들은 `$HOME/app/main.py`에 router를 추가한다. (ex. `app.include_router(users.router)`)
- **src**: 모듈 메인 기능
- unit test
  - 👉 유닛 테스트는 기본적으로 `$HOME/app`의 디렉토리 구조에 맞게 구성한다.
  - 유닛 테스트 종류로는 기능 테스트, API 엔드포인트 테스트, Pydantic 모델 유효성 테스트, 보안 테스트가 있다.
- **Dockerfile**
  - `Dockerfile`(=Dockerfile.dev 역할): 개발을 위해 필요한 도구 및 라이브러리와 같은 추가적인 종속성을 설치하기 위한 라이브러리들이 설치된 환경
  - `Dockerfile.prod`: 최종 제품을 배포하기 위해 필요한 것들만 포함한 환경


## Monolith
> @tiangolo 가 제공하는 유형(예: api, crud, 모델, 스키마)별로 파일을 구분하는 프로젝트 구조는 범위가 적은 마이크로 서비스 또는 프로젝트에 적합하지만 많은 도메인이 있는 모놀리식에는 맞출 수 없다.
> 더 확장 가능하고 진화할 수 있는 구조는 Netflix의 Dispatch 에서 영감을 얻었다.
- 출처: https://github.com/zhanymkanov/fastapi-best-practices


## 🚀 TODO
- [ ] **monolith** 개발 (현재 디렉터리만 생성되어있어 사용 불가능) 
- [ ] DB 적용한 API 동작 테스트
- [ ] Restful API 디자인 가이드: API token을 JWT token으로 설정
- [ ] Restful API 디자인 가이드: filtering, sorting, searching 기능을 query string으로 적용하기
- [ ] Restful API 디자인 가이드: 버전 관리 (버전별 URL 표기)
- [ ] Restful API 디자인 가이드: 링크 처리시 HATEOS를 이용한 링크 처리
- [ ] 에러 처리
- [ ] ELK 로그