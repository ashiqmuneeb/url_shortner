.PHONY: run test fmt lint docker-up docker-down

run:
	uvicorn app.main:app --reload --port 8000

test:
	pytest -q

fmt:
	python -m pip install black isort && black app tests && isort app tests

lint:
	python -m pip install ruff && ruff check app

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down
