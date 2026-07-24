"""Govern approved collection sources before a scraper can make requests."""
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any
import yaml


@dataclass(frozen=True)
class SourceProfile:
    name: str
    base_url: str
    collection_method: str
    status: str
    terms_reviewed_on: date | None
    robots_reviewed_on: date | None
    requests_per_minute: int
    notes: str = ""

    @property
    def is_approved(self) -> bool:
        return self.status == "approved"


def _parse_date(value: str | date | None) -> date | None:
    if not value:
        return None
    return value if isinstance(value, date) else date.fromisoformat(value)


def load_registry(path: str | Path) -> dict[str, SourceProfile]:
    """Load and validate source metadata from version-controlled YAML."""
    payload: dict[str, Any] = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    profiles = {}
    for item in payload.get("sources", []):
        profile = SourceProfile(
            name=item["name"], base_url=item["base_url"], collection_method=item["collection_method"],
            status=item["status"], terms_reviewed_on=_parse_date(item.get("terms_reviewed_on")),
            robots_reviewed_on=_parse_date(item.get("robots_reviewed_on")),
            requests_per_minute=int(item.get("requests_per_minute", 1)), notes=item.get("notes", ""),
        )
        if profile.name in profiles:
            raise ValueError(f"Duplicate source name: {profile.name}")
        profiles[profile.name] = profile
    return profiles


def require_approved_source(registry: dict[str, SourceProfile], source_name: str) -> SourceProfile:
    profile = registry.get(source_name)
    if profile is None:
        raise PermissionError(f"Source '{source_name}' is not registered.")
    if not profile.is_approved:
        raise PermissionError(f"Source '{source_name}' is '{profile.status}', not approved for collection.")
    return profile
