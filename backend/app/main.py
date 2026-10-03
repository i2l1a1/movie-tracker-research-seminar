from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app import models  # noqa: F401
from app.exception_handlers import register_exception_handlers
from app.middleware import register_request_timing
from app.routers import health, movies


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Movie Tracker", lifespan=lifespan)
register_request_timing(app)
register_exception_handlers(app)
app.include_router(health.router)
app.include_router(movies.router)
