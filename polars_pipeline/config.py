from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
REFERENCE_DIR = DATA_DIR / "reference"
PROCESSED_DIR = DATA_DIR / "processed"
WAREHOUSE_DIR = DATA_DIR / "warehouse"
DASHBOARD_DIR = PROJECT_ROOT / "dashboard"
DOCS_DIR = PROJECT_ROOT / "docs"

RAW_JOBS_PATH = RAW_DIR / "jobs_sample.csv"
OCCUPATION_REFERENCE_PATH = REFERENCE_DIR / "occupation_reference.csv"
MAJOR_SKILL_MAP_PATH = REFERENCE_DIR / "major_skill_map.csv"

WAREHOUSE_PATH = WAREHOUSE_DIR / "career_risk.duckdb"

