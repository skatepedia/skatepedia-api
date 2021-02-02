FROM python:3.8

ENV POETRY_VERSION=1.1.4

RUN apt-get update && apt-get install -y --no-install-recommends git curl

RUN pip install poetry=="$POETRY_VERSION"

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY scraper /app/scraper
COPY skatepedia /app/skatepedia

COPY manage.py /app/
COPY entrypoint.sh /app/


EXPOSE 9000

CMD ["bash", "entrypoint.sh"]
