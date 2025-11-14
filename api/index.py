"""Vercel Serverless Function Entry Point"""
import sys
import os

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

# Import Flask app
from app import app

# Export app for Vercel
# Vercel will automatically wrap this with WSGI handler
app = app
