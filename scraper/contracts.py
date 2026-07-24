"""Stable source-independent record contract for the raw data layer."""
from dataclasses import asdict, dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class RawJobPosting:
    source: str
    source_job_id: str
    url: str
    title: str
    company: str
    description: str | None = None
    location: str | None = None
    salary_text: str | None = None
    employment_type: str | None = None
    experience_text: str | None = None
    posted_text: str | None = None
    scraped_at: str = ""

    def to_dict(self) -> dict:
        payload = asdict(self)
        if not payload["scraped_at"]:
            payload["scraped_at"] = datetime.now(timezone.utc).isoformat()
        return payload
