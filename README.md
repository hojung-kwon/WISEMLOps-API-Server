## 프로젝트 환경 설정

```bash
# 쿠버네티스 클러스터 인증서 가져오기
cp ~/.kube/kubeconfig ./certs/kubeconfig

# 실행할 환경 설정 (default 값은 local)
export APP_ENV=local # local, container
```

## 프로젝트 실행

```bash
# 프로젝트 실행 
# 로컬
uvicorn main:app --reload
```

## Docker

```bash
# Docker 이미지 빌드
docker build -t registry.gitlab.com/wisenut-research/ctr/research/mlops/mlops-api .
```

```bash
# Docker 이미지 실행
docker run -it -p 8000:8000 registry.gitlab.com/wisenut-research/ctr/research/mlops/mlops-api
```