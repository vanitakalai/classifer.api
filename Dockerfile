FROM python:3.9.4-buster

WORKDIR /app
ENV PYTHONUNBUFFERED=1

RUN pip install poetry

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-dev

COPY ./classifier_api ./classifier_api

EXPOSE 8000

CMD ["uvicorn", "classifier_api.main:app", "--host", "0.0.0.0", "--port", "80", "--header", "server:classifier_api"]
