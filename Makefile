.PHONY: all test bench clean help

PYTHON ?= python3

help:
	@echo "Available targets:"
	@echo "  make test   - Run correctness test suite verifying all 5 engines"
	@echo "  make bench  - Run empirical RUM performance benchmark"
	@echo "  make clean  - Remove bytecode and cache files"

test:
	$(PYTHON) tests/test_all.py

bench:
	$(PYTHON) benchmarks/run.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.py[cod]" -delete
	rm -rf .pytest_cache
