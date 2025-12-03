#!/bin/bash
# Convenient launch script for Book of Psalms Database

set -e

echo "========================================="
echo "Book of Psalms Database"
echo "========================================="
echo ""

# Check if database exists
if [ ! -f "psalms.db" ]; then
    echo "Database not found. Initializing..."
    python seed.py
    echo ""
fi

# Launch Streamlit app
echo "Launching application..."
echo "Open your browser to http://localhost:8501"
echo ""
streamlit run app.py
