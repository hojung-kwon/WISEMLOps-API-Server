FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    vim

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.4.1 python3 -
# Set the working directory

WORKDIR /app

# copy src. see .dockerignore
COPY . .

# Install the dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --only main

# copy src. see .dockerignore
COPY . .

# Expose the port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]