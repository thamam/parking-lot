#!/bin/bash
# Quick verification script to test what works

set -e

cd "$(dirname "$0")/.."

echo "=================================================="
echo "  Serchify Test Verification"
echo "=================================================="
echo ""

echo "📦 Step 1: Installing dependencies..."
echo ""
if [ ! -d "node_modules" ]; then
    npm install --silent
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies already installed"
fi
echo ""

echo "=================================================="
echo "🧪 Step 2: Running Unit Tests"
echo "=================================================="
echo ""
npm run test:unit
echo ""

echo "=================================================="
echo "🔬 Step 3: Running Integration Tests (Real HTML)"
echo "=================================================="
echo ""
npx jest tests/integration/amazon-parser-real.test.js --verbose
echo ""

echo "=================================================="
echo "📊 Step 4: Coverage Report"
echo "=================================================="
echo ""
npm run test:coverage -- --silent
echo ""

echo "=================================================="
echo "✨ Verification Complete!"
echo "=================================================="
echo ""
echo "What was tested:"
echo "  ✅ Amazon URL parsing"
echo "  ✅ ASIN extraction"
echo "  ✅ Product data extraction (from real HTML structure)"
echo "  ✅ Price parsing"
echo "  ✅ Brand/category extraction"
echo "  ✅ Keyword generation"
echo "  ✅ Affiliate link handling"
echo "  ✅ Search query building"
echo ""
echo "What was NOT tested (requires API keys):"
echo "  ⚠️  Real marketplace API calls"
echo "  ⚠️  Actual product searches"
echo "  ⚠️  Live price comparisons"
echo ""
echo "Next steps:"
echo "  1. Review test results above"
echo "  2. Check coverage report in coverage/ directory"
echo "  3. See tests/README.md for more details"
echo "  4. To test in Chrome: Load extension from this directory"
echo ""
