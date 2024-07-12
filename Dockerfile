FROM python:3.12-slim

RUN pip install poetry==1.7.1

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY main.py /app

RUN poetry install

CMD ["poetry", "run", "python", "main.py"]