'''main.py'''
import time
import logging
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from db.database import init_db
from controllers.address_controller import router as address_router
from utilities.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    logger.info("Database initialized")
    yield


app = FastAPI(
    title="Address Book API",
    version="1.0.0",
    lifespan=lifespan,
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    '''
    Logs every incoming request and how it was handled: method, path,
    the status code returned, and how long it took. Gives a visible
    audit trail of everything hitting the API.
    '''
    start = time.time()
    response = await call_next(request)
    duration_ms = (time.time() - start) * 1000
    logger.info(
        f"{request.method} {request.url.path} -> {response.status_code} ({duration_ms:.1f}ms)"
    )
    return response


app.include_router(address_router)


@app.get("/")
def root():
    return {"message": "Address Book API is running"}