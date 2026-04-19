import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Import the actual Flask 'app' object from backend/app.py
from app import app

if __name__ == "__main__":
    app.run()
