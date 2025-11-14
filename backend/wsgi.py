"""
WSGI entry point for production deployment
"""
import os
import sys

# Ensure the backend directory is in the path
sys.path.insert(0, os.path.dirname(__file__))

from app import app

# Expose the Flask app for Gunicorn
application = app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
