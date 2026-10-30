import hashlib
import html
import json
import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from time import struct_time
from typing import Any, Callable
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

import feedparser

from app.integrations.sources.base import SourceDefinition

MAX_RESPONSE_BYTES = 2_000_000
REQUEST_TIMEOUT_SECONDS = 12


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def _plain_text(value: str, limit: int = 500) -> str:
    extractor = _TextExtractor()
    extractor.feed(value)
    text = " ".join(" ".join(extractor.parts).split())
    return html.unescape(text)[:limit]


def _parse_feed_date(value: Any) -> datetime | None:
    if isinstance(value, struct_time):
        return datetime(*value[:6], tzinfo=timezone.utc)
    if isinstance(value, str):
        try:
            parsed = parsedate_to_datetime(value)
        except (TypeError, ValueError, OverflowError):
            return None
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    return None


def _valid_item_url(value: str, source: SourceDefinition) -> str | None:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"}:
        return None
    if parsed.hostname not in {source.allowed_host, *source.allowed_link_hosts}:
        return None
    return value


def _make_item(
    source: SourceDefinition,
    *,
    external_id: str,
    title: str,
    summary: str,
    url: str,
    published_at: datetime | None,
) -> dict[str, Any] | None:
    safe_url = _valid_item_url(url, source)
    normalized_title = _plain_text(title, limit=240)
    if not safe_url or not normalized_title:
        return None

    stable_id = hashlib.sha256(
        f"{source.id}\0{external_id or safe_url}".encode("utf-8")
    ).hexdigest()
    return {
        "id": stable_id,
        "source_id": source.id,
        "source_name": source.name,
        "title": normalized_title,
        "summary": _plain_text(summary),
        "url": safe_url,
        "suggested_category_ids": list(source.suggested_category_ids),
        "scope": source.scope,
        "state_ids": list(source.state_ids),
        "item_type": source.item_type,
        "published_at": published_at,
        "status": "pending_review",
        "is_example": False,
        "imported_at": datetime.now(timezone.utc),
    }


def _parse_ibge_news(payload: bytes, source: SourceDefinition) -> list[dict[str, Any]]:
    data = json.loads(payload)
    records: list[dict[str, Any]] = []
    for entry in data.get("items", []):
        published_at = None
        date_text = entry.get("data_publicacao")
        if date_text:
            try:
                published_at = datetime.strptime(
                    date_text, "%d/%m/%Y %H:%M:%S"
                ).replace(tzinfo=ZoneInfo("America/Sao_Paulo")).astimezone(
                    timezone.utc
                )
            except ValueError:
                published_at = None

        item = _make_item(
            source,
            external_id=str(entry.get("id", "")),
            title=str(entry.get("titulo", "")),
            summary=str(entry.get("introducao", "")),
            url=str(entry.get("link", "")),
            published_at=published_at,
        )
        if item:
            records.append(item)
    return records


def _parse_rss(payload: bytes, source: SourceDefinition) -> list[dict[str, Any]]:
    parsed = feedparser.parse(payload)
    records: list[dict[str, Any]] = []
    for entry in parsed.entries:
        published_at = _parse_feed_date(
            entry.get("published_parsed")
            or entry.get("updated_parsed")
            or entry.get("published")
            or entry.get("updated")
        )
        item = _make_item(
            source,
            external_id=str(entry.get("id") or entry.get("guid") or ""),
            title=str(entry.get("title", "")),
            summary=str(entry.get("summary", "")),
            url=str(entry.get("link", "")),
            published_at=published_at,
        )
        if item:
            records.append(item)
    return records


def fetch_source_items(
    source: SourceDefinition,
    open_url: Callable[..., Any] = urlopen,
) -> list[dict[str, Any]]:
    request = Request(
        source.url,
        headers={"User-Agent": "HubBrasil/0.1 (+editorial source monitor)"},
    )
    try:
        with open_url(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            payload = response.read(MAX_RESPONSE_BYTES + 1)
    except (TimeoutError, URLError) as error:
        raise RuntimeError(f"Falha ao buscar fonte {source.id}.") from error

    if len(payload) > MAX_RESPONSE_BYTES:
        raise RuntimeError(f"Resposta acima do limite para a fonte {source.id}.")
    if source.format == "ibge_news":
        return _parse_ibge_news(payload, source)
    return _parse_rss(payload, source)