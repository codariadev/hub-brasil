import argparse
import json
import sys


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Importa metadados de fontes oficiais para revisão editorial."
    )
    parser.add_argument(
        "--source",
        action="append",
        dest="source_ids",
        help="ID da fonte para sincronizar; pode ser repetido.",
    )
    args = parser.parse_args()

    from app.integrations.sources.catalog import SOURCE_CATALOG

    sources = SOURCE_CATALOG
    if args.source_ids:
        requested = set(args.source_ids)
        sources = tuple(source for source in sources if source.id in requested)
        unknown = requested - {source.id for source in sources}
        if unknown:
            parser.error(f"Fontes desconhecidas: {', '.join(sorted(unknown))}")

    from app.integrations.firebase.firestore import get_source_items_collection
    from app.repositories.source_item_repository import SourceItemRepository
    from app.services.source_sync_service import sync_sources

    repository = SourceItemRepository(get_source_items_collection())
    result = sync_sources(repository, sources=sources)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    return 1 if any(source["error"] for source in result["sources"]) else 0


if __name__ == "__main__":
    sys.exit(main())