"""Load any raw JSONL data set through the same ETL pipeline."""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from etl.pipeline import load_jsonl

parser = argparse.ArgumentParser(description="Transform and load raw job records.")
parser.add_argument("path", type=Path, help="Path to a JSONL raw-data file")
args = parser.parse_args()
print(f"Loaded {load_jsonl(args.path)} records.")
