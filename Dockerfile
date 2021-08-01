FROM python:3.8-slim

WORKDIR /app
ENV PYTHONPATH "."
ENV PATH ".:${PATH}"

COPY poetry.lock /app/
COPY pyproject.toml /app/
RUN pip install poetry && \
    POETRY_VIRTUALENVS_CREATE=false poetry install
COPY . /app/

ENTRYPOINT ["docker-entrypoint.sh"]
