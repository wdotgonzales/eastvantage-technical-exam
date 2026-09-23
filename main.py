from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.database import init_db
from controllers.address_controller import router as address_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Address Book API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(address_router)


@app.get("/")
def root():
    return {"message": "Address Book API is running"}