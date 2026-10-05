from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Movie, MovieStatus, MovieType
from app.schemas import MovieCreate, MovieRead, MovieStats, MovieUpdate
from app.services.movies import MovieService, get_movie_service

router = APIRouter(prefix="/movies", tags=["movies"])


def provide_movie_service(db: Session = Depends(get_db)) -> MovieService:
    return get_movie_service(db)


@router.get("", response_model=list[MovieRead])
def list_movies(
    status_filter: MovieStatus | None = Query(default=None, alias="status"),
    type_filter: MovieType | None = Query(default=None, alias="type"),
    q: str | None = Query(default=None, min_length=1, max_length=255),
    service: MovieService = Depends(provide_movie_service),
) -> list[Movie]:
    return service.list_movies(status_filter=status_filter, type_filter=type_filter, q=q)


@router.post("", response_model=MovieRead, status_code=status.HTTP_201_CREATED)
def create_movie(
    payload: MovieCreate,
    service: MovieService = Depends(provide_movie_service),
) -> Movie:
    return service.create(payload)


@router.get("/stats", response_model=MovieStats)
def movies_stats(service: MovieService = Depends(provide_movie_service)) -> MovieStats:
    return service.stats()


@router.get("/upcoming", response_model=list[MovieRead])
def upcoming_movies(
    limit: int = Query(default=10, ge=1, le=100),
    status_filter: MovieStatus | None = Query(default=None, alias="status"),
    type_filter: MovieType | None = Query(default=None, alias="type"),
    q: str | None = Query(default=None, min_length=1, max_length=255),
    service: MovieService = Depends(provide_movie_service),
) -> list[Movie]:
    return service.upcoming(
        limit=limit,
        status_filter=status_filter,
        type_filter=type_filter,
        q=q,
    )


@router.get("/{movie_id}", response_model=MovieRead)
def get_movie(
    movie_id: int,
    service: MovieService = Depends(provide_movie_service),
) -> Movie:
    return service.get(movie_id)


@router.patch("/{movie_id}", response_model=MovieRead)
def update_movie(
    movie_id: int,
    payload: MovieUpdate,
    service: MovieService = Depends(provide_movie_service),
) -> Movie:
    return service.update(movie_id, payload)


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(
    movie_id: int,
    service: MovieService = Depends(provide_movie_service),
) -> None:
    service.delete(movie_id)
