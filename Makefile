.PHONY: install test lint scan docker-build docker-push ci clean

install:
	pip install -r requirements.txt ruff

test:
	pytest -v

lint:
	ruff check .

scan:
	trivy fs --severity HIGH,CRITICAL --exit-code 1 .

docker-build:
	docker build -t cicd-demo .

docker-push:
	docker push pavara/cicd-demo:latest

ci: lint test scan

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	rm -rf .pytest_cache
