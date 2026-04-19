import sys
import os

# Add the backend directory to the Python path
# This allows 'app.py' to find 'controllers' and 'utils' correctly
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app import app as application

if __name__ == "__main__":
    application.run()
