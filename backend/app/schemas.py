from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models import MovieStatus, MovieType


class MovieCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    type: MovieType
    status: MovieStatus
    rating: int | None = Field(default=None, ge=1, le=10)
    next_release_date: date | None = None

    @model_validator(mode="after")
    def validate_rating_for_status(self) -> "MovieCreate":
        if self.status == MovieStatus.planned and self.rating is not None:
            raise ValueError("rating is only allowed when status is watched")
        return self


class MovieUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    type: MovieType | None = None
    status: MovieStatus | None = None
    rating: int | None = Field(default=None, ge=1, le=10)
    next_release_date: date | None = None

    model_config = ConfigDict(extra="forbid")


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
