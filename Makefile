.PHONY: help install lint test cov check files secrets ci notebook clean

help:
	@echo "Sinusoid Extractor — common targets"
	@echo "  install   uv sync (install all deps incl. dev)"
	@echo "  lint      uv run ruff check"
	@echo "  test      uv run pytest"
	@echo "  cov       uv run pytest with coverage report"
	@echo "  files     enforce 150 LoC/file limit"
	@echo "  secrets   grep for hardcoded secrets"
	@echo "  ci        lint + test + cov + files + secrets"
	@echo "  notebook  execute analysis.ipynb headless"
	@echo "  clean     remove caches and pyc files"

install:
	uv sync

lint:
	uv run ruff check src tests

test:
	uv run pytest

cov:
	uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=85

files:
	uv run python scripts/check_file_lines.py

secrets:
	@! git grep -nE '(api_key|secret|password|token)\s*=\s*["'"'"']' src tests || (echo "FAIL: hardcoded secrets found"; exit 1)
	@echo "OK: no obvious hardcoded secrets"

ci: lint files secrets test cov
	@echo "All CI checks passed."

notebook:
	uv run jupyter nbconvert --to notebook --execute --inplace notebooks/analysis.ipynb

clean:
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete
	rm -rf .pytest_cache .ruff_cache .coverage htmlcov
