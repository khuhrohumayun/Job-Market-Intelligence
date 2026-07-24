"""Create the local database schema from the repository root or scripts directory."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from database.session import create_schema
create_schema()
print("Database schema created.")
