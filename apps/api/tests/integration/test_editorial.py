from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.api.v1.dependencies import get_editorial_repository
from app.core import security
from app.main import app


class FakeEditorialRepository:
    def __init__(self) -> None:
        self.published_by: str | None = None

    def list_pending_items(self) -> list[dict]:
        return [{"id": "source-1", "status": "pending_review"}]

    def publish_source_item(self, item_id: str, **fields: str) -> dict:
        self.published_by = fields["actor_email"]
        return {"id": item_id}


@pytest.fixture
def editorial_client() -> Iterator[tuple[TestClient, FakeEditorialRepository]]:
    repository = FakeEditorialRepository()
    app.dependency_overrides[get_editorial_repository] = lambda: repository
    with TestClient(app) as client:
        yield client, repository
    app.dependency_overrides.clear()


def test_editorial_queue_requires_authentication(
    editorial_client: tuple[TestClient, FakeEditorialRepository],
) -> None:
    client, _ = editorial_client

    response = client.get("/api/v1/editorial/source-items")

    assert response.status_code == 401


def test_editorial_queue_rejects_another_verified_email(
    editorial_client: tuple[TestClient, FakeEditorialRepository],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client, _ = editorial_client
    monkeypatch.setattr(
        security.auth,
        "verify_id_token",
        lambda token, check_revoked: {
            "email": "someone@example.com",
            "email_verified": True,
        },
    )

    response = client.get(
        "/api/v1/editorial/source-items",
        headers={"Authorization": "Bearer signed-token"},
    )

    assert response.status_code == 403


def test_editorial_queue_rejects_unverified_allowlisted_email(
    editorial_client: tuple[TestClient, FakeEditorialRepository],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client, _ = editorial_client
    monkeypatch.setattr(
        security.auth,
        "verify_id_token",
        lambda token, check_revoked: {
            "email": "alves2.eduardo@gmail.com",
            "email_verified": False,
        },
    )

    response = client.get(
        "/api/v1/editorial/source-items",
        headers={"Authorization": "Bearer signed-token"},
    )

    assert response.status_code == 403


def test_only_verified_allowlisted_email_can_publish(
    editorial_client: tuple[TestClient, FakeEditorialRepository],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client, repository = editorial_client
    monkeypatch.setattr(
        security.auth,
        "verify_id_token",
        lambda token, check_revoked: {
            "email": "alves2.eduardo@gmail.com",
            "email_verified": True,
        },
    )

    response = client.post(
        "/api/v1/editorial/source-items/source-1/publish",
        headers={"Authorization": "Bearer signed-token"},
        json={
            "title": "Mudança confirmada no serviço público",
            "summary": "Resumo revisado com contexto e impacto para a população.",
            "content": "Conteúdo editorial revisado com informações confirmadas, contexto, impacto para as pessoas e indicação clara da fonte consultada.",
            "category_id": "saude",
            "actor_email": "someone@example.com",
        },
    )

    assert response.status_code == 201
    assert response.json() == {"article_id": "source-1", "status": "published"}
    assert repository.published_by == "alves2.eduardo@gmail.com"