from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class SourceDefinition:
	id: str
	name: str
	url: str
	allowed_host: str
	format: Literal["rss", "ibge_news"]
	suggested_category_ids: tuple[str, ...]
	allowed_link_hosts: tuple[str, ...] = ()
	scope: Literal["national", "state"] = "national"
	state_ids: tuple[str, ...] = ()
	item_type: Literal["news", "alert"] = "news"
