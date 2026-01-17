#!/bin/bash
echo "========================================="
echo "PesaPal JuniorDB RDBMS"
echo "========================================="
echo ""
echo "Choose what to run:"
echo "1. Web Demo (Flask application)"
echo "2. REPL (Command Line Interface)"
echo "3. Tests"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo "Starting Web Demo..."
        source venv/bin/activate
        pip install flask > /dev/null 2>&1
        python3 web-demo/app.py
        ;;
    2)
        echo "Starting REPL..."
        source venv/bin/activate
        python3 main.py
        ;;
    3)
        echo "Running tests..."
        source venv/bin/activate
        python3 -m pytest tests/ -v
        ;;
    *)
        echo "Invalid choice"
        ;;
esac
