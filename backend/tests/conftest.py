import os

import pytest
from sqlalchemy import create_engine, text

_DB_HOST = "db" if os.path.exists("/.dockerenv") else "localhost"

ADMIN_DATABASE_URL = os.environ.get(
    "TEST_ADMIN_DATABASE_URL",
    f"postgresql+psycopg2://movie:movie@{_DB_HOST}:5432/movie_tracker",
)
TEST_DATABASE_NAME = "movie_tracker_test"
TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    f"postgresql+psycopg2://movie:movie@{_DB_HOST}:5432/{TEST_DATABASE_NAME}",
)


def _ensure_test_database() -> None:
    admin_engine = create_engine(ADMIN_DATABASE_URL, isolation_level="AUTOCOMMIT")
    with admin_engine.connect() as connection:
        exists = connection.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :name"),
            {"name": TEST_DATABASE_NAME},
        ).scalar()
        if not exists:
            connection.execute(text(f'CREATE DATABASE "{TEST_DATABASE_NAME}"'))
    admin_engine.dispose()


_ensure_test_database()
os.environ["DATABASE_URL"] = TEST_DATABASE_URL

from fastapi.testclient import TestClient  # noqa: E402

from app.database import Base, SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture()
def client():
    with SessionLocal() as session:
        session.execute(text("TRUNCATE TABLE movies RESTART IDENTITY CASCADE"))
        session.commit()

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
