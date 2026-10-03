from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions import MovieNotFoundError, MovieValidationError


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(MovieNotFoundError)
    async def movie_not_found_handler(_request: Request, _exc: MovieNotFoundError):
        return JSONResponse(status_code=404, content={"detail": "Movie not found"})

    @app.exception_handler(MovieValidationError)
    async def movie_validation_handler(_request: Request, exc: MovieValidationError):
        status_code = 400 if exc.message == "No fields to update" else 422
        return JSONResponse(status_code=status_code, content={"detail": exc.message})
