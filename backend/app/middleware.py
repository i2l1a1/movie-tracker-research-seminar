import logging
import time

from fastapi import FastAPI, Request

logger = logging.getLogger("movie_tracker.request")
if not logger.handlers:
    _handler = logging.StreamHandler()
    _handler.setFormatter(logging.Formatter("%(levelname)s:     %(message)s"))
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False


def register_request_timing(app: FastAPI) -> None:
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
