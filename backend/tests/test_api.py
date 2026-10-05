def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_movie(client):
    response = client.post(
        "/movies",
        json={
            "title": "Inception",
            "type": "movie",
            "status": "watched",
            "rating": 9,
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Inception"
    assert body["type"] == "movie"
    assert body["status"] == "watched"
    assert body["rating"] == 9
    assert body["id"] >= 1


def test_create_planned_with_rating_rejected(client):
    response = client.post(
        "/movies",
        json={
            "title": "Bad",
            "type": "movie",
            "status": "planned",
            "rating": 5,
        },
    )
    assert response.status_code == 422


def test_list_movies(client):
    client.post(
        "/movies",
        json={"title": "A", "type": "movie", "status": "watched", "rating": 7},
    )
    client.post(
        "/movies",
        json={
            "title": "B",
            "type": "series",
            "status": "planned",
            "next_release_date": "2027-01-01",
        },
    )
    response = client.get("/movies")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_list_filter_status_and_type(client):
    client.post(
        "/movies",
        json={"title": "Watched Movie", "type": "movie", "status": "watched", "rating": 8},
    )
    client.post(
        "/movies",
        json={"title": "Planned Series", "type": "series", "status": "planned"},
    )
    watched = client.get("/movies", params={"status": "watched"})
    assert watched.status_code == 200
    assert len(watched.json()) == 1
    assert watched.json()[0]["title"] == "Watched Movie"

    series = client.get("/movies", params={"type": "series"})
    assert series.status_code == 200
    assert len(series.json()) == 1
    assert series.json()[0]["title"] == "Planned Series"


def test_search_by_title_substring(client):
    client.post(
        "/movies",
        json={"title": "Interstellar", "type": "movie", "status": "watched", "rating": 10},
    )
    client.post(
        "/movies",
        json={"title": "Dune", "type": "movie", "status": "watched", "rating": 8},
    )
    response = client.get("/movies", params={"q": "Inter"})
    assert response.status_code == 200
    titles = [item["title"] for item in response.json()]
    assert titles == ["Interstellar"]


def test_get_movie(client):
    created = client.post(
        "/movies",
        json={"title": "Dune", "type": "movie", "status": "watched", "rating": 8},
    ).json()
    response = client.get(f"/movies/{created['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Dune"


def test_get_movie_not_found(client):
    response = client.get("/movies/999999")
    assert response.status_code == 404


def test_patch_movie(client):
    created = client.post(
        "/movies",
        json={"title": "Old", "type": "movie", "status": "planned"},
    ).json()
    response = client.patch(
        f"/movies/{created['id']}",
        json={"status": "watched", "rating": 6, "title": "New"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "New"
    assert body["status"] == "watched"
    assert body["rating"] == 6


def test_patch_movie_not_found(client):
    response = client.patch("/movies/999999", json={"title": "X"})
    assert response.status_code == 404


def test_delete_movie(client):
    created = client.post(
        "/movies",
        json={"title": "Delete me", "type": "movie", "status": "watched", "rating": 5},
    ).json()
    response = client.delete(f"/movies/{created['id']}")
    assert response.status_code == 204
    assert client.get(f"/movies/{created['id']}").status_code == 404


def test_delete_movie_not_found(client):
    response = client.delete("/movies/999999")
    assert response.status_code == 404


def test_stats(client):
    client.post(
        "/movies",
        json={"title": "M1", "type": "movie", "status": "watched", "rating": 8},
    )
    client.post(
        "/movies",
        json={"title": "S1", "type": "series", "status": "planned"},
    )
    response = client.get("/movies/stats")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert body["watched"] == 1
    assert body["planned"] == 1
    assert body["movies"] == 1
    assert body["series"] == 1
    assert body["average_rating"] == 8.0


def test_upcoming(client):
    client.post(
        "/movies",
        json={
            "title": "Later",
            "type": "series",
            "status": "planned",
            "next_release_date": "2027-06-01",
        },
    )
    client.post(
        "/movies",
        json={
            "title": "Soon",
            "type": "movie",
            "status": "planned",
            "next_release_date": "2026-10-01",
        },
    )
    client.post(
        "/movies",
        json={"title": "No date", "type": "movie", "status": "watched", "rating": 7},
    )
    response = client.get("/movies/upcoming")
    assert response.status_code == 200
    titles = [item["title"] for item in response.json()]
    assert titles == ["Soon", "Later"]

    limited = client.get("/movies/upcoming", params={"limit": 1})
    assert limited.status_code == 200
    assert len(limited.json()) == 1
    assert limited.json()[0]["title"] == "Soon"

    by_type = client.get("/movies/upcoming", params={"type": "movie"})
    assert by_type.status_code == 200
    assert [item["title"] for item in by_type.json()] == ["Soon"]

    by_q = client.get("/movies/upcoming", params={"q": "lat"})
    assert by_q.status_code == 200
    assert [item["title"] for item in by_q.json()] == ["Later"]
