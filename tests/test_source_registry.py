from pathlib import Path
import pytest
from scraper.source_registry import load_registry, require_approved_source

ROOT = Path(__file__).resolve().parents[1]

def test_registry_allows_synthetic_data_only():
    registry = load_registry(ROOT / "config/sources.yaml")
    assert require_approved_source(registry, "synthetic_demo").is_approved

def test_registry_blocks_unapproved_source():
    registry = load_registry(ROOT / "config/sources.yaml")
    with pytest.raises(PermissionError):
        require_approved_source(registry, "linkedin")
