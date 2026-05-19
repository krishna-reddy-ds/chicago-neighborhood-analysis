#!/bin/bash

echo "=========================================="
echo "CS 579 Final Project Setup"
echo "=========================================="

# Check Python version
echo ""
echo "[1/4] Checking Python version..."
python --version

# Install core dependencies
echo ""
echo "[2/4] Installing core dependencies..."
pip install numpy pandas matplotlib seaborn networkx scikit-learn requests --quiet

# Install optional dependencies
echo ""
echo "[3/4] Installing optional dependencies..."
pip install folium --quiet
echo "  - folium installed (for interactive maps)"

# Try to install Leiden
echo ""
pip install leidenalg python-igraph --quiet 2>/dev/null
if [ $? -eq 0 ]; then
    echo "  - leidenalg installed (for advanced community detection)"
else
    echo "  - leidenalg installation failed (optional, will use Louvain only)"
fi

# Check Census API key
echo ""
echo "[4/4] Checking Census API key..."
if [ -z "$CENSUS_API_KEY" ]; then
    echo "  WARNING: CENSUS_API_KEY environment variable not set!"
    echo "  Get your key from: https://api.census.gov/data/key_signup.html"
    echo "  Then run: export CENSUS_API_KEY='your_key_here'"
else
    echo "  Census API key found: ${CENSUS_API_KEY:0:10}..."
fi

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. If you haven't already, set your Census API key:"
echo "     export CENSUS_API_KEY='your_key_here'"
echo ""
echo "  2. Run the project:"
echo "     python final_project_complete.py"
echo ""
echo "=========================================="