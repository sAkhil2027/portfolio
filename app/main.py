"""
Application entrypoint runner script using FastAPI and Uvicorn.
"""

import os
import uvicorn
from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Akhil's FastAPI Portfolio app on http://127.0.0.1:{port}")
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
