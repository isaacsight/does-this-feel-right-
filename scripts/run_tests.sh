#!/bin/bash
# Test Execution Script
# Runs the full test suite with coverage reporting

set -e

echo "🧪 Running Test Suite..."
echo ""

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run pytest with coverage
echo "Running tests with coverage..."
pytest \
    --cov=. \
    --cov-report=html \
    --cov-report=term-missing \
    --cov-report=term:skip-covered \
    -v \
    tests/

echo ""
echo "✓ Tests complete!"
echo ""
echo "Coverage report generated in: htmlcov/index.html"
echo "Open with: open htmlcov/index.html"
echo ""
