"""Tests d'intégration — endpoints Events (Concert, Théâtre, Conférence)."""

from httpx import AsyncClient

_EVENTS_URL = "/api/v1/events"


def _concert_payload(
    venue_id: str,
    organizer_id: str,
    slug_suffix: str = "",
) -> dict[str, object]:
    return {
        "event_type": "concert",
        "title": f"Jazz Festival Paris 2025{slug_suffix}",
        "slug": f"jazz-festival-paris-2025{slug_suffix}",
        "start_at": "2025-07-14T20:00:00+02:00",
        "end_at": "2025-07-14T23:30:00+02:00",
        "city": "Paris",
        "price": "45.00",
        "capacity": 500,
        "venue_public_id": venue_id,
        "organizer_public_id": organizer_id,
        "artist": "Ibrahim Maalouf",
        "genre": "Jazz contemporain",
    }


def _theatre_payload(
    venue_id: str,
    organizer_id: str,
    slug_suffix: str = "",
) -> dict[str, object]:
    return {
        "event_type": "theatre",
        "title": f"Hamlet{slug_suffix}",
        "slug": f"hamlet{slug_suffix}",
        "start_at": "2025-08-01T19:00:00+02:00",
        "end_at": "2025-08-01T21:30:00+02:00",
        "city": "Lyon",
        "venue_public_id": venue_id,
        "organizer_public_id": organizer_id,
        "director": "Ariane Mnouchkine",
        "cast_members": "Sophie Marceau, Vincent Cassel",
    }


def _conference_payload(
    venue_id: str,
    organizer_id: str,
    slug_suffix: str = "",
) -> dict[str, object]:
    return {
        "event_type": "conference",
        "title": f"IA & Créativité{slug_suffix}",
        "slug": f"ia-creativite{slug_suffix}",
        "start_at": "2025-09-10T09:00:00+02:00",
        "end_at": "2025-09-10T17:00:00+02:00",
        "city": "Paris",
        "venue_public_id": venue_id,
        "organizer_public_id": organizer_id,
        "speaker": "Pr. Jean Dupont",
        "topic": "Intelligence Artificielle et Créativité",
    }


# ── Lecture publique ──────────────────────────────────────────────────────────


async def test_list_events_public(client: AsyncClient) -> None:
    response = await client.get(_EVENTS_URL)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data


async def test_list_events_pagination(client: AsyncClient) -> None:
    response = await client.get(f"{_EVENTS_URL}?page=1&size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["size"] == 10


async def test_get_event_introuvable(client: AsyncClient) -> None:
    response = await client.get(
        f"{_EVENTS_URL}/00000000-0000-0000-0000-000000000000"
    )
    assert response.status_code == 404


# ── Création sans auth ────────────────────────────────────────────────────────


async def test_create_event_sans_auth(
    client: AsyncClient,
    seed_venue: str,
    seed_organizer: str,
) -> None:
    payload = _concert_payload(seed_venue, seed_organizer, "-noauth")
    response = await client.post(_EVENTS_URL, json=payload)
    assert response.status_code == 401


# ── Création Concert ──────────────────────────────────────────────────────────


async def test_create_concert_succes(
    client: AsyncClient,
    admin_token: str,
    seed_venue: str,
    seed_organizer: str,
) -> None:
    payload = _concert_payload(seed_venue, seed_organizer, "-create")
    response = await client.post(
        _EVENTS_URL,
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["event_type"] == "concert"
    assert data["artist"] == "Ibrahim Maalouf"
    assert data["city"] == "Paris"
    assert "public_id" in data


# ── Création Théâtre ──────────────────────────────────────────────────────────


async def test_create_theatre_succes(
    client: AsyncClient,
    admin_token: str,
    seed_venue: str,
    seed_organizer: str,
) -> None:
    payload = _theatre_payload(seed_venue, seed_organizer, "-create")
    response = await client.post(
        _EVENTS_URL,
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["event_type"] == "theatre"
    assert data["director"] == "Ariane Mnouchkine"


# ── Création Conférence ───────────────────────────────────────────────────────


async def test_create_conference_succes(
    client: AsyncClient,
    admin_token: str,
    seed_venue: str,
    seed_organizer: str,
) -> None:
    payload = _conference_payload(seed_venue, seed_organizer, "-create")
    response = await client.post(
        _EVENTS_URL,
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["event_type"] == "conference"
    assert data["speaker"] == "Pr. Jean Dupont"


# ── Validation métier ─────────────────────────────────────────────────────────


async def test_create_event_dates_invalides(
    client: AsyncClient,
    admin_token: str,
    seed_venue: str,
    seed_organizer: str,
) -> None:
    payload = _concert_payload(seed_venue, seed_organizer, "-bad-dates")
    payload["end_at"] = "2025-07-14T18:00:00+02:00"  # antérieure à start_at
    response = await client.post(
        _EVENTS_URL,
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 422


async def test_create_event_slug_duplique(
    client: AsyncClient,
    admin_token: str,
    seed_venue: str,
    seed_organizer: str,
) -> None:
    payload = _concert_payload(seed_venue, seed_organizer, "-dup")
    await client.post(
        _EVENTS_URL,
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    response = await client.post(
        _EVENTS_URL,
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 409


async def test_create_event_image_invalide(
    client: AsyncClient,
    admin_token: str,
    seed_venue: str,
    seed_organizer: str,
) -> None:
    payload = _concert_payload(seed_venue, seed_organizer, "-bad-img")
    payload["image_url"] = "http://example.com/image.bmp"  # HTTP + extension invalide
    response = await client.post(
        _EVENTS_URL,
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 422


# ── Lecture d'un événement ────────────────────────────────────────────────────


async def test_get_event_succes(
    client: AsyncClient,
    admin_token: str,
    seed_venue: str,
    seed_organizer: str,
) -> None:
    created = await client.post(
        _EVENTS_URL,
        json=_concert_payload(seed_venue, seed_organizer, "-get"),
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    public_id = created.json()["public_id"]

    response = await client.get(f"{_EVENTS_URL}/{public_id}")
    assert response.status_code == 200
    assert response.json()["public_id"] == public_id
    assert response.json()["event_type"] == "concert"


# ── Filtres avancés ───────────────────────────────────────────────────────────


async def test_list_events_filtre_city(client: AsyncClient) -> None:
    response = await client.get(f"{_EVENTS_URL}?city=Paris")
    assert response.status_code == 200


async def test_list_events_filtre_event_type(client: AsyncClient) -> None:
    response = await client.get(f"{_EVENTS_URL}?event_type=concert")
    assert response.status_code == 200
    data = response.json()
    for item in data["items"]:
        assert item["event_type"] == "concert"


async def test_list_events_filtre_price_max(client: AsyncClient) -> None:
    response = await client.get(f"{_EVENTS_URL}?price_max=50")
    assert response.status_code == 200
    data = response.json()
    for item in data["items"]:
        if item.get("price") is not None:
            assert float(item["price"]) <= 50


async def test_list_events_filtre_tags(client: AsyncClient) -> None:
    response = await client.get(f"{_EVENTS_URL}?tags=jazz")
    assert response.status_code == 200


async def test_list_events_tri_price_desc(client: AsyncClient) -> None:
    response = await client.get(f"{_EVENTS_URL}?sort_by=price&sort_order=desc")
    assert response.status_code == 200


# ── Mise à jour ───────────────────────────────────────────────────────────────


async def test_update_event_succes(
    client: AsyncClient,
    admin_token: str,
    seed_venue: str,
    seed_organizer: str,
) -> None:
    created = await client.post(
        _EVENTS_URL,
        json=_concert_payload(seed_venue, seed_organizer, "-update"),
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    public_id = created.json()["public_id"]

    response = await client.patch(
        f"{_EVENTS_URL}/{public_id}",
        json={"title": "Jazz Festival Mis à Jour", "city": "Marseille"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Jazz Festival Mis à Jour"
    assert data["city"] == "Marseille"


async def test_update_event_sans_auth(
    client: AsyncClient,
    admin_token: str,
    seed_venue: str,
    seed_organizer: str,
) -> None:
    created = await client.post(
        _EVENTS_URL,
        json=_concert_payload(seed_venue, seed_organizer, "-update-noauth"),
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    public_id = created.json()["public_id"]

    response = await client.patch(
        f"{_EVENTS_URL}/{public_id}",
        json={"city": "Nice"},
    )
    assert response.status_code == 401


# ── Suppression ───────────────────────────────────────────────────────────────


async def test_delete_event_succes(
    client: AsyncClient,
    admin_token: str,
    seed_venue: str,
    seed_organizer: str,
) -> None:
    created = await client.post(
        _EVENTS_URL,
        json=_concert_payload(seed_venue, seed_organizer, "-delete"),
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    public_id = created.json()["public_id"]

    response = await client.delete(
        f"{_EVENTS_URL}/{public_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 204

    response = await client.get(f"{_EVENTS_URL}/{public_id}")
    assert response.status_code == 404


async def test_delete_event_sans_auth(
    client: AsyncClient,
    admin_token: str,
    seed_venue: str,
    seed_organizer: str,
) -> None:
    created = await client.post(
        _EVENTS_URL,
        json=_concert_payload(seed_venue, seed_organizer, "-delete-noauth"),
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    public_id = created.json()["public_id"]

    response = await client.delete(f"{_EVENTS_URL}/{public_id}")
    assert response.status_code == 401
