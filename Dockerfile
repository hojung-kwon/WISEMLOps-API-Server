FROM python:3.10.11-slim

# Set environment variables
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=utf-8
ENV LOG_LEVEL=DEBUG

# 작업 디렉토리 설정
WORKDIR /home/wisenut/app

# Certs 경로 설정
ENV CERTS_PATH=/home/wisenut/app/certs/

# 파이썬 실행 위치
ENV PYTHONPATH=/home/wisenut/app:${PYTHONPATH}

# 필요한 파일 복사
COPY requirements.txt .
COPY ./src ./src/

# 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 8000

# Run the app
CMD ["python", "src/main.py"]