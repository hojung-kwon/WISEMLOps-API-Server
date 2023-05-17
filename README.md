## 프로젝트 환경 설정

```bash
# X509 인증서 추출
kubectl config view --minify --raw --output \
'jsonpath={..cluster.certificate-authority-data}' \
| base64 -d > k8s-ca.cert

# 클러스터 관리자 계정 토큰 발급
kubectl create token default --duration=0 > bearer_token

# 위 파일들을 프로젝트 내 /certs 폴더로 이동
CERTS_PATH=${/certs 폴더 절대경로} # 프로젝트 환경변수 설정
```

## 프로젝트 실행

```bash
# 프로젝트 실행 
# 로컬
python main.py

# Docker
docker-compose up [--build]
```