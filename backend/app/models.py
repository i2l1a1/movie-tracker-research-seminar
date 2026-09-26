import enum
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class MovieType(str, enum.Enum):
    movie = "movie"
    series = "series"


class MovieStatus(str, enum.Enum):
    watched = "watched"
    planned = "planned"


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[MovieType] = mapped_column(Enum(MovieType, name="movie_type"), nullable=False)
    status: Mapped[MovieStatus] = mapped_column(
        Enum(MovieStatus, name="movie_status"), nullable=False
    )
    rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    next_release_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
