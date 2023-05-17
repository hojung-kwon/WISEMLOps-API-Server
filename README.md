## 프로젝트 환경 설정

```bash
# 쿠버네티스 클러스터 인증서 가져오기
cd ~/.kube/config ./kubeconfig

# 위 파일들을 프로젝트 내 /certs 폴더로 이동
mv ./kubeconfig ./certs/kubeconfig

# 실행할 환경 설정
export APP_ENV=local # local, dev, prod
```

## 프로젝트 실행

```bash
# 프로젝트 실행 
# 로컬
python main.py

# Docker
docker-compose up [--build]
```