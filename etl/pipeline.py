"""Orchestrates extract/transform/load and commits one safe batch."""
import json
from pathlib import Path
from app.logging import get_logger
from database.repository import upsert_job
from database.session import SessionLocal, create_schema
from etl.transform import transform
from nlp.skills import SkillExtractor

logger = get_logger(__name__)

def load_jsonl(path: str | Path) -> int:
    create_schema(); extractor = SkillExtractor(); loaded = 0
    with Path(path).open(encoding="utf-8") as source, SessionLocal() as session:
        for line in source:
            raw = json.loads(line)
            cleaned = transform(raw, extractor.extract(raw.get("title", "") + " " + raw.get("description", "")))
            if not cleaned.get("source_job_id") or not cleaned.get("title") or not cleaned.get("company"):
                logger.warning("Skipping incomplete record: %s", raw.get("url")); continue
            upsert_job(session, cleaned); loaded += 1
        session.commit()
    logger.info("Loaded %s records", loaded)
    return loaded
