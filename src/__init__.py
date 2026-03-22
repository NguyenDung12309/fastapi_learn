from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.app import api_router
from src.db.main import init_db


@asynccontextmanager
async def life_span(app: FastAPI):
    print("server is running...")
    init_db()
    yield
    print("server is done...")

version ="v1"
app = FastAPI(
    title="Book API",
    description="Book API",
    version=version,
    lifespan=life_span,
)

app.include_router(api_router, prefix="/api/v1")