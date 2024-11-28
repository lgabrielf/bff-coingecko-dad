FROM python:3.10-slim

RUN pip install --no-cache-dir poetry==1.5.1 

RUN mkdir /app
WORKDIR /app

COPY src/ ./src
COPY poetry.lock pyproject.toml /app/
COPY README.md ./

RUN poetry config virtualenvs.create false
RUN poetry install

EXPOSE 8080
