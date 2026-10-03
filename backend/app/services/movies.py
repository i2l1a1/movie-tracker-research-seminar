from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.exceptions import MovieNotFoundError, MovieValidationError
from app.models import Movie, MovieStatus, MovieType
from app.rules import resolve_rating
from app.schemas import MovieCreate, MovieStats, MovieUpdate


class MovieService:
    def __init__(self, db: Session) -> None:
        self._db = db

    def list_movies(
        self,
        *,
        status_filter: MovieStatus | None = None,
        type_filter: MovieType | None = None,
        q: str | None = None,
    ) -> list[Movie]:
        query = select(Movie).order_by(Movie.id)
        if status_filter is not None:
            query = query.where(Movie.status == status_filter)
        if type_filter is not None:
            query = query.where(Movie.type == type_filter)
        if q is not None:
            query = query.where(Movie.title.ilike(f"%{q}%"))
        return list(self._db.scalars(query).all())

    def get(self, movie_id: int) -> Movie:
        return self._require_movie(movie_id)

    def create(self, payload: MovieCreate) -> Movie:
        try:
            rating = resolve_rating(payload.status, payload.rating, rating_provided=True)
        except ValueError as exc:
            raise MovieValidationError(str(exc)) from exc

        movie = Movie(
            title=payload.title,
            type=payload.type,
            status=payload.status,
            rating=rating,
            next_release_date=payload.next_release_date,
        )
        self._db.add(movie)
        self._db.commit()
        self._db.refresh(movie)
        return movie

    def update(self, movie_id: int, payload: MovieUpdate) -> Movie:
        movie = self._require_movie(movie_id)
        data = payload.model_dump(exclude_unset=True)
        if not data:
            raise MovieValidationError("No fields to update")

        new_status = data.get("status", movie.status)
        rating_provided = "rating" in data
        new_rating = data["rating"] if rating_provided else movie.rating

        try:
            resolved_rating = resolve_rating(
                new_status,
                new_rating,
                rating_provided=rating_provided or new_status == MovieStatus.planned,
            )
        except ValueError as exc:
            raise MovieValidationError(str(exc)) from exc

        for field, value in data.items():
            if field == "rating":
                continue
            setattr(movie, field, value)
        movie.rating = resolved_rating

        self._db.commit()
        self._db.refresh(movie)
        return movie

    def delete(self, movie_id: int) -> None:
        movie = self._require_movie(movie_id)
        self._db.delete(movie)
        self._db.commit()

    def stats(self) -> MovieStats:
        row = self._db.execute(
            select(
                func.count().label("total"),
                func.count().filter(Movie.status == MovieStatus.watched).label("watched"),
                func.count().filter(Movie.status == MovieStatus.planned).label("planned"),
                func.count().filter(Movie.type == MovieType.movie).label("movies"),
                func.count().filter(Movie.type == MovieType.series).label("series"),
                func.avg(Movie.rating).label("average_rating"),
            ).select_from(Movie)
        ).one()

        average = row.average_rating
        return MovieStats(
            total=row.total or 0,
            watched=row.watched or 0,
            planned=row.planned or 0,
            movies=row.movies or 0,
            series=row.series or 0,
            average_rating=round(float(average), 2) if average is not None else None,
        )

    def upcoming(self, *, limit: int = 10) -> list[Movie]:
        query = (
            select(Movie)
            .where(Movie.next_release_date.is_not(None))
            .order_by(Movie.next_release_date.asc(), Movie.id.asc())
            .limit(limit)
        )
        return list(self._db.scalars(query).all())

    def _require_movie(self, movie_id: int) -> Movie:
        movie = self._db.get(Movie, movie_id)
        if movie is None:
            raise MovieNotFoundError()
        return movie


def get_movie_service(db: Session) -> MovieService:
    return MovieService(db)
