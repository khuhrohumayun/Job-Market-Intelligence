"""Pure transformations: deterministic, testable, and reusable across sources."""
from datetime import datetime
import html
import re
from typing import Any

CITY_ALIASES = {"islamabad capital territory": "Islamabad", "lahore, pakistan": "Lahore", "karachi, pakistan": "Karachi"}

def clean_text(value: str | None) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(value or ""))).strip()

def normalize_city(value: str | None) -> str | None:
    if not value:
        return None
    cleaned = clean_text(value).lower()
    return CITY_ALIASES.get(cleaned, cleaned.title())

def parse_date(value: str | None):
    if not value:
        return None
    for pattern in ("%Y-%m-%d", "%d %b %Y", "%d/%m/%Y"):
        try: return datetime.strptime(value.strip(), pattern).date()
        except ValueError: pass
    return None

def parse_salary(value: str | None) -> dict[str, Any] | None:
    if not value: return None
    numbers = [float(n.replace(",", "")) for n in re.findall(r"\d[\d,]*", value)]
    if not numbers: return None
    return {"min_amount": numbers[0], "max_amount": numbers[-1] if len(numbers) > 1 else None,
            "currency": "PKR" if "pkr" in value.lower() or "rs" in value.lower() else "PKR", "period": "monthly"}

def transform(record: dict, skills: list[str]) -> dict:
    return {**record, "title": clean_text(record.get("title")), "company": clean_text(record.get("company")),
            "description": clean_text(record.get("description")), "city": normalize_city(record.get("city")),
            "posted_at": parse_date(record.get("posted_at")), "salary": parse_salary(record.get("salary")), "skills": sorted(set(skills))}
