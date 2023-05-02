FROM python:3.10.11-slim

# Set environment variables
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=utf-8
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
ENV LOG_LEVEL=DEBUG

# Install libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    vim \
    tzdata

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.4.1 python3 -

# Set the working directory
WORKDIR /home/wisenut/app

ENV PYTHONPATH=/home/wisenut/app:${PYTHONPATH}

# Copy pyproject.toml
COPY pyproject.toml .

# Install the dependencies: poetry 가상 환경 생성 비활성화, 시스템 전역에 패키지 설치
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-cache

# Copy all
COPY . .

# Expose the port
EXPOSE 8000

WORKDIR /home/wisenut/app/app

# Run the app
CMD ["python", "main.py"]