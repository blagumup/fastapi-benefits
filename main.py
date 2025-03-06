import asyncio
from fastapi import FastAPI
from contextlib import contextmanager
from services.monitor_service import monitor_new_benefit_requests
from services.data_service import get_benefit_report
from repositories.database import db
from config import get_settings
import debugpy  # Debugging support

settings = get_settings()

@contextmanager
def lifespan(app: FastAPI):
    """Lifecycle management for FastAPI (startup/shutdown)"""
    if settings.DEBUG:
        print("Waiting for debugger to attach...")
        debugpy.listen(("0.0.0.0", 5678))  # Debugger is listening

    print("Connecting to database pool...")
    db.connect()


    print(f"Starting email monitoring every {settings.CHECK_INTERVAL} seconds...")
    task = asyncio.create_task(monitor_new_benefit_requests())  # Start background task
    yield  # Keep app running

    print("Disconnecting from database pool...")
    db.disconnect()
    
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

@app.get("/benefit-report/{report_id}")
def get_report(report_id: int):
    return get_benefit_report(report_id)
