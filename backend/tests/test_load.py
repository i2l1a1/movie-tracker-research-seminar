import time

import pytest
from sqlalchemy import text

from app.database import SessionLocal

LOAD_SIZE = 100_000


def _elapsed_ms(started: float) -> float:
    return (time.perf_counter() - started) * 1000


@pytest.mark.load
def test_load_movies(client):
    print(f"\n=== LOAD TEST: {LOAD_SIZE} movies ===")

    with SessionLocal() as session:
        session.execute(text("TRUNCATE TABLE movies RESTART IDENTITY CASCADE"))
        session.commit()

        started = time.perf_counter()
        session.execute(
            text(
                """
                INSERT INTO movies (
                    title, type, status, rating, next_release_date, created_at, updated_at
                )
                SELECT
                    'Title ' || g,
                    CASE WHEN g % 2 = 0 THEN 'movie' ELSE 'series' END::movie_type,
                    CASE WHEN g % 3 = 0 THEN 'planned' ELSE 'watched' END::movie_status,
                    CASE WHEN g % 3 = 0 THEN NULL ELSE ((g % 10) + 1) END,
                    CASE
                        WHEN g % 5 = 0
                        THEN DATE '2026-01-01' + ((g % 400) * INTERVAL '1 day')
                        ELSE NULL
                    END,
                    NOW(),
                    NOW()
                FROM generate_series(1, :n) AS g
                """
            ),
            {"n": LOAD_SIZE},
        )
        session.commit()
        insert_ms = _elapsed_ms(started)

    count = client.get("/movies/stats").json()["total"]
    assert count == LOAD_SIZE
    print(f"[LOAD] bulk insert {LOAD_SIZE} rows: {insert_ms:.1f} ms ({insert_ms / 1000:.1f} s)")

    started = time.perf_counter()
    stats = client.get("/movies/stats")
    stats_ms = _elapsed_ms(started)
    assert stats.status_code == 200
    body = stats.json()
    assert body["total"] == LOAD_SIZE
    print(f"[LOAD] GET /movies/stats: {stats_ms:.1f} ms -> {body}")

    started = time.perf_counter()
    search = client.get("/movies", params={"q": "Title 77777"})
    search_ms = _elapsed_ms(started)
    assert search.status_code == 200
    assert len(search.json()) == 1
    assert search.json()[0]["title"] == "Title 77777"
    print(f"[LOAD] GET /movies?q=Title 77777: {search_ms:.1f} ms")

    started = time.perf_counter()
    filtered = client.get(
        "/movies",
        params={"status": "planned", "type": "series", "q": "Title 99999"},
    )
    filter_ms = _elapsed_ms(started)
    assert filtered.status_code == 200
    assert len(filtered.json()) == 1
    print(
        f"[LOAD] GET /movies?status=planned&type=series&q=Title 99999: "
        f"{filter_ms:.1f} ms (hits={len(filtered.json())})"
    )

    started = time.perf_counter()
    upcoming = client.get("/movies/upcoming", params={"limit": 20})
    upcoming_ms = _elapsed_ms(started)
    assert upcoming.status_code == 200
    assert len(upcoming.json()) == 20
    print(f"[LOAD] GET /movies/upcoming?limit=20: {upcoming_ms:.1f} ms")

    target_id = 50_000
    started = time.perf_counter()
    one = client.get(f"/movies/{target_id}")
    get_ms = _elapsed_ms(started)
    assert one.status_code == 200
    print(f"[LOAD] GET /movies/{target_id}: {get_ms:.1f} ms")

    started = time.perf_counter()
    patched = client.patch(
        f"/movies/{target_id}",
        json={"title": "Patched Under Load", "rating": 10, "status": "watched"},
    )
    patch_ms = _elapsed_ms(started)
    assert patched.status_code == 200
    assert patched.json()["title"] == "Patched Under Load"
    print(f"[LOAD] PATCH /movies/{target_id}: {patch_ms:.1f} ms")

    started = time.perf_counter()
    created = client.post(
        "/movies",
        json={
            "title": "After Load Create",
            "type": "movie",
            "status": "watched",
            "rating": 9,
        },
    )
    create_ms = _elapsed_ms(started)
    assert created.status_code == 201
    created_id = created.json()["id"]
    print(f"[LOAD] POST /movies: {create_ms:.1f} ms (id={created_id})")

    started = time.perf_counter()
    deleted = client.delete(f"/movies/{created_id}")
    delete_ms = _elapsed_ms(started)
    assert deleted.status_code == 204
    print(f"[LOAD] DELETE /movies/{created_id}: {delete_ms:.1f} ms")

    started = time.perf_counter()
    stats_after = client.get("/movies/stats")
    stats_after_ms = _elapsed_ms(started)
    assert stats_after.status_code == 200
    assert stats_after.json()["total"] == LOAD_SIZE
    print(f"[LOAD] GET /movies/stats (after): {stats_after_ms:.1f} ms")

    with SessionLocal() as session:
        session.execute(text("TRUNCATE TABLE movies RESTART IDENTITY CASCADE"))
        session.commit()
    print("[LOAD] table movies truncated after test")

    print("=== LOAD TEST DONE ===")
