FROM python:3.8-slim

WORKDIR /app
ENV PYTHONPATH "."
ENV PATH ".:${PATH}"

COPY Pipfile* /app/
RUN pip install pipenv && \
    pipenv install --system --deploy
COPY . /app/

ENTRYPOINT ["docker-entrypoint.sh"]
