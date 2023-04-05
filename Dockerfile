FROM python:3.10-slim

# Set environment variables
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul
ENV PYTHONUNBUFFERED=1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    vim \
    tzdata

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.4.1 python3 -

# Create user (Error - Permission denied: poetry.lock)
#RUN groupadd -g 1012 wisenut
#RUN useradd wisenut -u 1012 -g wisenut -m -s /bin/bash
#USER wisenut

# Set the working directory
WORKDIR /home/wisenut/app

# copy src. see .dockerignore
COPY . .

# Install the dependencies: poetry 가상 환경 생성 비활성화, 시스템 전역에 패키지 설치
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy poetry
COPY . .

# Expose the port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]