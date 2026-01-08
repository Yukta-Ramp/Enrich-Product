import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from app.main import app

print("Registered Routes:")
for route in app.routes:
    print(f"- {route.path} [{route.name}]")
