#!/bin/bash
# Development Environment Setup Script
# This script sets up a complete development environment for the blog project

set -e  # Exit on error

echo "🚀 Setting up Blog Development Environment..."
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or later."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet

# Install production dependencies
echo "📚 Installing production dependencies..."
pip install -r requirements.txt --quiet
echo "✓ Production dependencies installed"

# Install development dependencies
echo "🛠️  Installing development dependencies..."
pip install -r requirements-dev.txt --quiet
echo "✓ Development dependencies installed"

# Setup pre-commit hooks
echo "🪝 Setting up pre-commit hooks..."
pre-commit install
echo "✓ Pre-commit hooks installed"

# Create .env from template if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your API keys!"
    echo "   The file is located at: $(pwd)/.env"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "🎉 Development environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment: source .venv/bin/activate"
echo "2. Edit .env and add your API keys"
echo "3. Run tests: pytest"
echo "4. Start building: python build.py"
echo ""
