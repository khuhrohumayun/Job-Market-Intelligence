"""Generate transparent, deterministic test data for load and dashboard testing."""
import argparse
import json
import random
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

CITIES = ["Karachi", "Lahore", "Islamabad", "Rawalpindi", "Faisalabad", "Peshawar", "Remote"]
COMPANIES = ["Nexa Systems", "PakData Labs", "Orbit AI", "BluePeak Technologies", "Vertex Digital", "CloudCraft PK", "Insight Forge"]
ROLES = {
    "Data Engineer": ["python", "sql", "data engineering", "spark", "aws", "docker"],
    "Data Scientist": ["python", "machine learning", "pandas", "tensorflow", "sql"],
    "Machine Learning Engineer": ["python", "machine learning", "pytorch", "docker", "kubernetes"],
    "BI Analyst": ["sql", "power bi", "tableau", "pandas"],
    "Analytics Engineer": ["python", "sql", "data engineering", "docker", "aws"],
}
EMPLOYMENT_TYPES = ["Full-time", "Contract", "Hybrid", "Remote"]
EXPERIENCE = ["Entry", "Mid", "Senior"]


def generate_record(index: int, rng: random.Random, start_date: date) -> dict:
    title = rng.choice(list(ROLES))
    role_skills = rng.sample(ROLES[title], k=rng.randint(3, len(ROLES[title])))
    posted_at = start_date + timedelta(days=rng.randrange(365))
    minimum = rng.randrange(90_000, 280_000, 10_000)
    maximum = minimum + rng.randrange(40_000, 150_000, 10_000)
    return {
        "source": "synthetic_demo",
        "source_job_id": f"synthetic-{index:07d}",
        "url": f"https://example.invalid/jobs/{index}",
        "title": title,
        "company": rng.choice(COMPANIES),
        "description": f"Synthetic test posting for a {title}. Required skills: {', '.join(role_skills)}.",
        "city": rng.choice(CITIES),
        "salary": f"PKR {minimum:,} - {maximum:,}",
        "employment_type": rng.choice(EMPLOYMENT_TYPES),
        "experience_level": rng.choice(EXPERIENCE),
        "posted_at": posted_at.isoformat(),
        "is_synthetic": True,
    }


def generate(output: Path, count: int, seed: int) -> Path:
    rng = random.Random(seed)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as target:
        for index in range(1, count + 1):
            target.write(json.dumps(generate_record(index, rng, date(2025, 7, 1))) + "\n")
    manifest = output.with_suffix(".manifest.json")
    manifest.write_text(json.dumps({"dataset": output.name, "record_count": count, "seed": seed, "synthetic": True,
                                    "warning": "Test data only; not representative of the Pakistan job market."}, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Create synthetic job data for performance and UI testing.")
    parser.add_argument("--count", type=int, default=1_000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=ROOT / "data/raw/synthetic_jobs.jsonl")
    args = parser.parse_args()
    if args.count < 1:
        parser.error("--count must be positive")
    manifest = generate(args.output, args.count, args.seed)
    print(f"Generated {args.count:,} synthetic records: {args.output}")
    print(f"Manifest: {manifest}")


if __name__ == "__main__":
    main()
