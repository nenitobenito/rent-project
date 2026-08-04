from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_INTERIM = PROJECT_ROOT / "data" / "interim"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"

ADDRESSBASE_ZIP_DIR = DATA_RAW / "addressbase"
ADDRESSBASE_EXTRACT_DIR = DATA_INTERIM / "addressbase"