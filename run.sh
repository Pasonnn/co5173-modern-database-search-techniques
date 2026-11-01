#!/usr/bin/env bash
set -e

CMD=${1:-"help"}

case "$CMD" in
  test)
    echo "Running search technique test suite..."
    python3 tests/test_all.py
    ;;
  bench)
    echo "Running comparative empirical benchmarks..."
    python3 benchmarks/run.py
    ;;
  stress)
    echo "Running workload stress-testing suite (Section 4.2)..."
    python3 benchmarks/stress_test.py
    ;;
  clean)
    echo "Cleaning Python cache files..."
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.py[cod]" -delete 2>/dev/null || true
    ;;
  *)
    echo "Usage: ./run.sh [test|bench|clean]"
    exit 1
    ;;
esac
