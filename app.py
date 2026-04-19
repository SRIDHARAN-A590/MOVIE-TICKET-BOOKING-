import sys
import os

# Add the backend directory to the Python path
# This allows 'main.py' to find 'controllers' and 'utils' correctly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import the actual Flask 'app' object from backend/main.py
from main import app

if __name__ == "__main__":
    app.run()
