# GitHub Init Command - Development Makefile

.PHONY: test test-fast test-unit test-integration install-deps lint format check clean help

# Default target
help:
	@echo "Available targets:"
	@echo "  test          - Run all tests (< 1 minute)"
	@echo "  test-fast     - Run only fast unit tests (< 5 seconds)"
	@echo "  test-unit     - Run unit tests only"
	@echo "  test-integration - Run integration tests only"
	@echo "  lint          - Run all linters"
	@echo "  format        - Format code with black and isort"
	@echo "  check         - Run syntax and import checks"
	@echo "  install-deps  - Install test dependencies"
	@echo "  clean         - Clean up test artifacts"

# Install test dependencies
install-deps:
	pip install -r requirements-test.txt

# Run all tests with coverage
test:
	pytest test_fast.py test_integration_fast.py test_github_init_command.py \
		--cov=github_init_command \
		--cov=register_command \
		--cov-report=term-missing \
		--tb=short

# Run only the fastest tests for quick feedback
test-fast:
	pytest test_fast.py::TestFastGitHubInitOptions \
	       test_fast.py::TestFastArgumentParsing \
	       --tb=line -v

# Run unit tests only
test-unit:
	pytest test_fast.py --tb=short

# Run integration tests only  
test-integration:
	pytest test_integration_fast.py test_github_init_command.py --tb=short

# Linting
lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	mypy github_init_command.py register_command.py --ignore-missing-imports

# Code formatting
format:
	black .
	isort .

# Quick syntax and import checks
check:
	python -m py_compile github_init_command.py
	python -m py_compile register_command.py
	python -c "import test_fast, test_integration_fast, test_github_init_command"

# Clean up
clean:
	rm -rf .pytest_cache/
	rm -rf __pycache__/
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf htmlcov/
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete

# For CI: validate everything quickly
ci-fast:
	@echo "Running fast CI validation..."
	make check
	make test-fast
	@echo "✅ Fast CI validation completed successfully!"

# For CI: full validation
ci-full:
	@echo "Running full CI validation..."
	make check
	make lint  
	make test
	@echo "✅ Full CI validation completed successfully!"