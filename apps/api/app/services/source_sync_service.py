from collections.abc import Callable, Sequence
from typing import Any

from app.integrations.sources.base import SourceDefinition
from app.integrations.sources.catalog import SOURCE_CATALOG
from app.integrations.sources.rss import fetch_source_items


def sync_sources(
    repository: Any,
    sources: Sequence[SourceDefinition] = SOURCE_CATALOG,
    fetcher: Callable[[SourceDefinition], list[dict[str, Any]]] = fetch_source_items,
) -> dict[str, Any]:
    result: dict[str, Any] = {"sources": [], "fetched": 0, "created": 0}

    for source in sources:
        source_result: dict[str, Any] = {
            "source_id": source.id,
            "source_name": source.name,
            "fetched": 0,
            "created": 0,
            "error": None,
        }
        try:
            items = fetcher(source)
            source_result["fetched"] = len(items)
            result["fetched"] += len(items)
            if items:
                created = repository.save_new(items)
                source_result["created"] = created
                result["created"] += created
        except Exception as error:
            source_result["error"] = str(error)
        result["sources"].append(source_result)

    return result