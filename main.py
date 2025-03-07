import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from services.monitor_service import monitor_new_benefit_requests
from services.data_service import get_compensation_request, get_benefit_categories, get_employees, get_employee, get_compensation_requests
from repositories.database import db
from config import get_settings
import debugpy  # Debugging support

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
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

@app.get('/compensation_requests')
def compensation_requests_get():
    return get_compensation_requests()

@app.get("/compensation_request/{request_id}")
def compensation_request_get(report_id: int):
    return get_compensation_request(report_id)


@app.get("/benefit_categories")
def benefit_categories_get():
    return get_benefit_categories()


@app.get("/employees")
def employees_get():
    return get_employees()

@app.get("/employee/{employee_id}")
def employee_get(employee_id: str):
    return get_employee(employee_id)