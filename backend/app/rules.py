from app.models import MovieStatus


def resolve_rating(
    status: MovieStatus,
    rating: int | None,
    *,
    rating_provided: bool,
) -> int | None:
    if status == MovieStatus.planned:
        if rating_provided and rating is not None:
            raise ValueError("rating is only allowed when status is watched")
        return None
    return rating
