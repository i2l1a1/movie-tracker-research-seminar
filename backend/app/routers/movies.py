from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Movie, MovieStatus, MovieType
from app.schemas import MovieCreate, MovieRead, MovieStats, MovieUpdate

router = APIRouter(prefix="/movies", tags=["movies"])


def _apply_rating_rules(
    *,
    status_value: MovieStatus,
    rating: int | None,
    rating_provided: bool,
) -> int | None:
    if status_value == MovieStatus.planned:
        if rating_provided and rating is not None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="rating is only allowed when status is watched",
            )
        return None
    return rating


@router.get("", response_model=list[MovieRead])
def list_movies(
    status_filter: MovieStatus | None = Query(default=None, alias="status"),
    type_filter: MovieType | None = Query(default=None, alias="type"),
    db: Session = Depends(get_db),
) -> list[Movie]:
    query = select(Movie).order_by(Movie.id)
    if status_filter is not None:
        query = query.where(Movie.status == status_filter)
    if type_filter is not None:
        query = query.where(Movie.type == type_filter)
    return list(db.scalars(query).all())


@router.post("", response_model=MovieRead, status_code=status.HTTP_201_CREATED)
def create_movie(payload: MovieCreate, db: Session = Depends(get_db)) -> Movie:
    movie = Movie(
        title=payload.title,
        type=payload.type,
        status=payload.status,
        rating=_apply_rating_rules(
            status_value=payload.status,
            rating=payload.rating,
            rating_provided=True,
        ),
        next_release_date=payload.next_release_date,
    )
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie


@router.get("/stats", response_model=MovieStats)
def movies_stats(db: Session = Depends(get_db)) -> MovieStats:
    total = db.scalar(select(func.count()).select_from(Movie)) or 0
    watched = (
        db.scalar(select(func.count()).select_from(Movie).where(Movie.status == MovieStatus.watched))
        or 0
    )
    planned = (
        db.scalar(select(func.count()).select_from(Movie).where(Movie.status == MovieStatus.planned))
        or 0
    )
    movies_count = (
        db.scalar(select(func.count()).select_from(Movie).where(Movie.type == MovieType.movie)) or 0
    )
    series_count = (
        db.scalar(select(func.count()).select_from(Movie).where(Movie.type == MovieType.series))
        or 0
    )
    average_rating = db.scalar(
        select(func.avg(Movie.rating)).where(Movie.rating.is_not(None))
    )
    return MovieStats(
        total=total,
        watched=watched,
        planned=planned,
        movies=movies_count,
        series=series_count,
        average_rating=round(float(average_rating), 2) if average_rating is not None else None,
    )


@router.get("/upcoming", response_model=list[MovieRead])
def upcoming_movies(
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[Movie]:
    query = (
        select(Movie)
        .where(Movie.next_release_date.is_not(None))
        .order_by(Movie.next_release_date.asc(), Movie.id.asc())
        .limit(limit)
    )
    return list(db.scalars(query).all())


@router.get("/{movie_id}", response_model=MovieRead)
def get_movie(movie_id: int, db: Session = Depends(get_db)) -> Movie:
    movie = db.get(Movie, movie_id)
    if movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return movie


@router.patch("/{movie_id}", response_model=MovieRead)
def update_movie(
    movie_id: int,
    payload: MovieUpdate,
    db: Session = Depends(get_db),
) -> Movie:
    movie = db.get(Movie, movie_id)
    if movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

    data = payload.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    new_status = data.get("status", movie.status)
    rating_provided = "rating" in data
    new_rating = data["rating"] if rating_provided else movie.rating

    resolved_rating = _apply_rating_rules(
        status_value=new_status,
        rating=new_rating,
        rating_provided=rating_provided or new_status == MovieStatus.planned,
    )

    for field, value in data.items():
        if field == "rating":
            continue
        setattr(movie, field, value)
    movie.rating = resolved_rating

    db.commit()
    db.refresh(movie)
    return movie


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int, db: Session = Depends(get_db)) -> None:
    movie = db.get(Movie, movie_id)
    if movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    db.delete(movie)
    db.commit()
