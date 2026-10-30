from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_categories_endpoint_returns_product_categories() -> None:
    response = client.get("/api/v1/categories")

    assert response.status_code == 200
    categories = response.json()
    assert len(categories) == 6
    assert categories[0]["id"] == "economia"


def test_articles_endpoint_marks_development_content_as_examples(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "development")
    monkeypatch.delenv("GOOGLE_APPLICATION_CREDENTIALS", raising=False)

    response = client.get("/api/v1/articles")

    assert response.status_code == 200
    articles = response.json()
    assert len(articles) == 2
    assert all(article["is_example"] is True for article in articles)


def test_articles_endpoint_does_not_return_examples_in_production(
    monkeypatch,
) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setattr(
        "app.api.v1.endpoints.articles.get_firestore_client",
        lambda: None,
    )
    monkeypatch.setattr(
        "app.api.v1.endpoints.articles.ArticleRepository",
        lambda client: type("EmptyRepository", (), {"list_published": lambda self: []})(),
    )

    response = client.get("/api/v1/articles")

    assert response.status_code == 200
    assert response.json() == []


def test_articles_endpoint_does_not_return_examples_without_environment(
    monkeypatch,
) -> None:
    monkeypatch.delenv("APP_ENV", raising=False)
    monkeypatch.setattr(
        "app.api.v1.endpoints.articles.get_firestore_client",
        lambda: None,
    )
    monkeypatch.setattr(
        "app.api.v1.endpoints.articles.ArticleRepository",
        lambda client: type("EmptyRepository", (), {"list_published": lambda self: []})(),
    )

    response = client.get("/api/v1/articles")

    assert response.status_code == 200
    assert response.json() == []