"""CLI entry point for an approved source configuration."""
import argparse
import json
from pathlib import Path
from scraper.configurable_bs4 import ConfigurableBeautifulSoupScraper, SelectorConfig
from scraper.jsonl_sink import JsonlSink

def main() -> None:
    parser = argparse.ArgumentParser(description="Crawl an approved static job-listing source.")
    parser.add_argument("config", type=Path)
    parser.add_argument("--pages", type=int, default=1)
    parser.add_argument("--output", type=Path, default=Path("data/raw/jobs.jsonl"))
    args = parser.parse_args()
    config = SelectorConfig(**json.loads(args.config.read_text(encoding="utf-8")))
    count = ConfigurableBeautifulSoupScraper(config).crawl_approved(JsonlSink(args.output), args.pages)
    print(f"Saved {count} records to {args.output}")

if __name__ == "__main__": main()
