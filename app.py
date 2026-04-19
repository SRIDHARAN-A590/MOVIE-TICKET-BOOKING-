import sys
import os
import traceback

try:
    # Ensure we use an absolute path so it works regardless of the execution context
    backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend'))
    if backend_path not in sys.path:
        sys.path.insert(0, backend_path)

    # Import the actual Flask 'app' object from backend/main.py
    from main import app
except Exception as e:
    print("CRITICAL IMPORT ERROR IN app.py:")
    traceback.print_exc()
    raise

if __name__ == "__main__":
    app.run()
