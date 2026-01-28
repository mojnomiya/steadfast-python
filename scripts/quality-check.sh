#!/bin/bash
# Quality check script - runs all code quality checks

set -e

echo "🔍 Running code quality checks..."

# Activate virtual environment
source venv/bin/activate

# Run pre-commit on all files
echo "📋 Running pre-commit hooks..."
pre-commit run --all-files

echo "✅ All quality checks passed!"
