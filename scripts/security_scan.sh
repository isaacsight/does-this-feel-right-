#!/bin/bash
# Security Scan Script
# Runs comprehensive security checks on the codebase

set -e

echo "🔒 Running Security Scans..."
echo ""

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Check for vulnerable dependencies
echo "1️⃣  Checking for vulnerable dependencies with pip-audit..."
pip-audit || echo "⚠️  Vulnerabilities found! Review above output."
echo ""

# Scan code for security issues
echo "2️⃣  Scanning code for security issues with bandit..."
bandit -r . -ll --skip B101 -x .venv,venv,build,dist,.eggs || echo "⚠️  Security issues found! Review above output."
echo ""

# Check for known security issues in dependencies
echo "3️⃣  Checking dependency safety with safety..."
safety check || echo "⚠️  Unsafe dependencies found! Review above output."
echo ""

# Check for exposed secrets
echo "4️⃣  Checking for exposed secrets..."
if grep -r "sk-" --include="*.py" --exclude-dir=".venv" . 2>/dev/null; then
    echo "⚠️  Possible API keys found in code!"
else
    echo "✓ No obvious API keys in code"
fi

echo ""
echo "🔒 Security scan complete!"
echo ""
