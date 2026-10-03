from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models import MovieStatus, MovieType
from app.rules import resolve_rating


class MovieCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    type: MovieType
    status: MovieStatus
    rating: int | None = Field(default=None, ge=1, le=10)
    next_release_date: date | None = None

    @model_validator(mode="after")
    def validate_rating_for_status(self) -> "MovieCreate":
        resolve_rating(self.status, self.rating, rating_provided=True)
        return self


class MovieUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    type: MovieType | None = None
    status: MovieStatus | None = None
    rating: int | None = Field(default=None, ge=1, le=10)
    next_release_date: date | None = None

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def validate_rating_for_status(self) -> "MovieUpdate":
        if self.status == MovieStatus.planned and self.rating is not None:
            resolve_rating(self.status, self.rating, rating_provided=True)
        return self


class MovieRead(BaseModel):
    id: int
    title: str
    type: MovieType
    status: MovieStatus
    rating: int | None
    next_release_date: date | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MovieStats(BaseModel):
    total: int
    watched: int
    planned: int
    movies: int
    series: int
    average_rating: float | None
