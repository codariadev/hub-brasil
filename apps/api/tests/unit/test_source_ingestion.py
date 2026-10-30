from io import BytesIO

from app.integrations.sources.base import SourceDefinition
from app.integrations.sources.catalog import SOURCE_CATALOG
from app.integrations.sources.rss import fetch_source_items
from app.services.source_sync_service import sync_sources


class FakeCollection:
    def __init__(self) -> None:
        self.items: dict[str, dict] = {}

    def document(self, item_id: str):
        collection = self

        class Document:
            def create(self, item: dict) -> None:
                if item_id in collection.items:
                    from google.api_core.exceptions import AlreadyExists

                    raise AlreadyExists("Item already imported")
                collection.items[item_id] = item

        return Document()


class FakeResponse(BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *args) -> None:
        self.close()


def test_rss_import_stores_metadata_only_and_marks_for_review() -> None:
    source = next(item for item in SOURCE_CATALOG if item.id == "noticias-sc")
    feed = b"""<?xml version="1.0"?>
    <rss version="2.0"><channel><title>Noticias SC</title>
      <item><guid>post-1</guid><title>Alerta de exemplo</title>
        <link>https://noticias.sc.gov.br/post-1/</link>
        <description>&lt;p&gt;Resumo oficial.&lt;/p&gt;</description>
        <pubDate>Thu, 29 Oct 2026 12:00:00 +0000</pubDate>
      </item>
    </channel></rss>"""

    items = fetch_source_items(
        source,
        open_url=lambda request, timeout: FakeResponse(feed),
    )

    assert len(items) == 1
    assert items[0]["status"] == "pending_review"
    assert items[0]["scope"] == "state"
    assert items[0]["state_ids"] == ["SC"]
    assert items[0]["summary"] == "Resumo oficial."
    assert "content" not in items[0]


def test_ibge_api_response_is_normalized_to_a_source_item() -> None:
    source = next(item for item in SOURCE_CATALOG if item.id == "ibge-news")
    payload = b"""{"items":[{"id":42,"titulo":"Indicador divulgado",
      "introducao":"Resumo do release","link":"http://agenciadenoticias.ibge.gov.br/noticia/42",
      "data_publicacao":"29/10/2026 12:00:00"}]}"""

    items = fetch_source_items(
        source,
        open_url=lambda request, timeout: FakeResponse(payload),
    )

    assert len(items) == 1
    assert items[0]["source_id"] == "ibge-news"
    assert items[0]["status"] == "pending_review"


def test_external_links_from_unapproved_hosts_are_discarded() -> None:
    source = next(item for item in SOURCE_CATALOG if item.id == "ministerio-saude")
    feed = b"""<rss version="2.0"><channel>
      <item><guid>x</guid><title>External</title>
        <link>https://example.com/noticia</link>
      </item></channel></rss>"""

    items = fetch_source_items(
        source,
        open_url=lambda request, timeout: FakeResponse(feed),
    )

    assert items == []


def test_rdf_feed_used_by_ibama_is_parsed() -> None:
        source = next(item for item in SOURCE_CATALOG if item.id == "ibama")
        feed = b"""<?xml version="1.0"?>
        <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
            xmlns="http://purl.org/rss/1.0/" xmlns:dc="http://purl.org/dc/elements/1.1/">
            <channel rdf:about="https://www.gov.br/ibama/pt-br/RSS">
                <title>IBAMA</title><link>https://www.gov.br/ibama/pt-br</link>
                <items><rdf:Seq><rdf:li rdf:resource="https://www.gov.br/ibama/pt-br/noticia" />
                </rdf:Seq></items>
            </channel>
            <item rdf:about="https://www.gov.br/ibama/pt-br/noticia">
                <title>Fiscaliza&#231;&#227;o ambiental</title>
                <link>https://www.gov.br/ibama/pt-br/noticia</link>
                <description>Atualiza&#231;&#227;o oficial.</description>
                <dc:date>2026-10-29T12:00:00Z</dc:date>
            </item>
        </rdf:RDF>"""

        items = fetch_source_items(
                source,
                open_url=lambda request, timeout: FakeResponse(feed),
        )

        assert len(items) == 1
        assert items[0]["source_id"] == "ibama"
        assert items[0]["title"] == "Fiscalização ambiental"


def test_sync_deduplicates_existing_items_and_continues_after_failure() -> None:
    source = SOURCE_CATALOG[0]
    collection = FakeCollection()
    items = [{"id": "stable-item"}]

    class Repository:
        def save_new(self, received: list[dict]) -> int:
            created = 0
            for item in received:
                if item["id"] not in collection.items:
                    collection.items[item["id"]] = item
                    created += 1
            return created

    def fetcher(selected: SourceDefinition) -> list[dict]:
        if selected.id == "broken":
            raise RuntimeError("Feed indisponível")
        return items

    result = sync_sources(
        Repository(),
        sources=(source, SourceDefinition(
            id="broken",
            name="Fonte indisponível",
            url="https://example.gov.br/feed",
            allowed_host="example.gov.br",
            format="rss",
            suggested_category_ids=("saude",),
        )),
        fetcher=fetcher,
    )

    assert result["created"] == 1
    assert result["sources"][1]["error"] == "Feed indisponível"