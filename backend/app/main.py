from contextlib import asynccontextmanager
import logging
import time

from fastapi import FastAPI, Request
from sqlalchemy import text

from app.database import Base, engine
from app import models  # noqa: F401
from app.routers import movies

logger = logging.getLogger("movie_tracker.request")
if not logger.handlers:
    _handler = logging.StreamHandler()
    _handler.setFormatter(logging.Formatter("%(levelname)s:     %(message)s"))
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Movie Tracker", lifespan=lifespan)
app.include_router(movies.router)


@app.middleware("http")
async def log_request_time(request: Request, call_next):
    started = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - started) * 1000

    path = request.url.path
    if request.url.query:
        path = f"{path}?{request.url.query}"

    route = request.scope.get("route")
    route_path = getattr(route, "path", None)
    route_part = f" [{route_path}]" if route_path and route_path != request.url.path else ""

    logger.info(
        "[TIME] %s %s%s -> %s in %.1f ms",
        request.method,
        path,
        route_part,
        response.status_code,
        elapsed_ms,
    )
    return response


@app.get("/health", tags=["health"])
def health_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "ok"}
