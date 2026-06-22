"""Tests d'intégration — endpoints Organizers."""

from httpx import AsyncClient

_ORGANIZERS_URL = "/api/v1/organizers"


def _org_payload(suffix: str = "") -> dict[str, object]:
    return {
        "name": f"Productions du Sud{suffix}",
        "email": f"contact{suffix.replace(' ', '')}@productions-sud.fr",
        "telephone": "+22890123456",
        "description": "Producteur d'événements culturels.",
    }


async def test_list_organizers_public(client: AsyncClient) -> None:
    response = await client.get(_ORGANIZERS_URL)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data


async def test_create_organizer_sans_auth(client: AsyncClient) -> None:
    response = await client.post(_ORGANIZERS_URL, json=_org_payload("-noauth"))
    assert response.status_code == 401


async def test_create_organizer_succes(client: AsyncClient, admin_token: str) -> None:
    response = await client.post(
        _ORGANIZERS_URL,
        json=_org_payload("-create"),
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Productions du Sud-create"
    assert "public_id" in data
    assert "email" in data


async def test_get_organizer_succes(client: AsyncClient, admin_token: str) -> None:
    created = await client.post(
        _ORGANIZERS_URL,
        json=_org_payload("-get"),
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    public_id = created.json()["public_id"]

    response = await client.get(f"{_ORGANIZERS_URL}/{public_id}")
    assert response.status_code == 200
    assert response.json()["public_id"] == public_id


async def test_get_organizer_introuvable(client: AsyncClient) -> None:
    response = await client.get(
        f"{_ORGANIZERS_URL}/00000000-0000-0000-0000-000000000000"
    )
    assert response.status_code == 404


async def test_update_organizer_succes(client: AsyncClient, admin_token: str) -> None:
    created = await client.post(
        _ORGANIZERS_URL,
        json=_org_payload("-update"),
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    public_id = created.json()["public_id"]

    response = await client.patch(
        f"{_ORGANIZERS_URL}/{public_id}",
        json={"name": "Nouveau Nom"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Nouveau Nom"


async def test_delete_organizer_succes(client: AsyncClient, admin_token: str) -> None:
    created = await client.post(
        _ORGANIZERS_URL,
        json=_org_payload("-delete"),
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    public_id = created.json()["public_id"]

    response = await client.delete(
        f"{_ORGANIZERS_URL}/{public_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 204

    response = await client.get(f"{_ORGANIZERS_URL}/{public_id}")
    assert response.status_code == 404


async def test_telephone_invalide(client: AsyncClient, admin_token: str) -> None:
    payload = _org_payload("-bad-tel")
    payload["telephone"] = "0612345678"
    response = await client.post(
        _ORGANIZERS_URL,
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 422


async def test_pagination_organizers(client: AsyncClient) -> None:
    response = await client.get(f"{_ORGANIZERS_URL}?page=1&size=5")
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["size"] == 5
