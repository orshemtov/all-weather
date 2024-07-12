install:
	poetry install

run:
	poetry run python main.py

test:
	poetry run pytest -s -vv

build:
	docker build -t all-weather .

run-docker:
	docker run all-weather