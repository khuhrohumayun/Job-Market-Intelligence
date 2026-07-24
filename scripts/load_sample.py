"""Load the shipped sample dataset."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from etl.pipeline import load_jsonl
print(f"Loaded {load_jsonl(ROOT / 'data/raw/sample_jobs.jsonl')} records.")
