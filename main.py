import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from services.email_service import monitor_email
from config import get_settings
import debugpy  # Debugging support

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management for FastAPI (startup/shutdown)"""
    if settings.DEBUG:
        print("Waiting for debugger to attach...")
        debugpy.listen(("0.0.0.0", 5678))  # Debugger is listening

    print(f"Starting email monitoring every {settings.CHECK_INTERVAL} seconds...")
    task = asyncio.create_task(monitor_email())  # Start background task
    yield  # Keep app running
    task.cancel()

app = FastAPI(
    debug=True,
    lifespan=lifespan
)

@app.get("/")
def root():
    return {"message": "FastAPI is running with email monitoring!"}




# @app.get("/benefits")
# def get_benefits():
#     return

# @app.get("/benefits/{user_id}")
# def get_benefits(user_id: int):
#     return {"user_id": user_id, "benefits": "Sample Benefit Data"}
