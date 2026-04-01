from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from sqlmodel import SQLModel
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.api import api_router
from src.core.exceptions import AppError
from src.db.main import db_manager


def verify_token():
    print("Check token")


class FastAPIServer:
    def __init__(self):
        self._app = FastAPI(
            debug=True,
            title="Book Management",
            summary="book api documentation",
            description="all book in here",
            version="0.0.1",
            openapi_url="/api/v1/openapi.json",
            servers=[{"url": "http://localhost:8000", "description": "Local"}],
            dependencies=[Depends(verify_token)],
            docs_url="/docs",
            redoc_url="/redoc",
            middleware=[
                Middleware(
                    CORSMiddleware,
                    allow_origins=["*"],
                    allow_methods=["*"],
                    allow_headers=["*"],
                )
            ],
            lifespan=self._lifespan_context
        )
        self._setup_routers()
        self._setup_exception_handlers()

    def _setup_routers(self):
        self._app.include_router(api_router, prefix="/api/v1")

    def _setup_exception_handlers(self):

        @self._app.exception_handler(AppError)
        def app_error_handler(request: Request, exc: AppError):
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "status": "error",
                    "code": exc.status_code,
                    "message": exc.message
                }
            )

    @staticmethod
    def _init_db():
        SQLModel.metadata.create_all(db_manager.engine)
        try:
            with db_manager.engine.connect() as conn:
                print("database connected")
        except Exception as e:
            print("database connection failed: {e}")
            raise e

    @asynccontextmanager
    async def _lifespan_context(self, app: FastAPI):
        print("🚀 start")
        self._init_db()
        yield
        print("🛑 stop")
        db_manager.close_connections()

    @property
    def app(self):
        return self._app


server = FastAPIServer()
app = server.app
