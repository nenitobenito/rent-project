from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIRECTORY = PROJECT_ROOT / "data"
ADDRESS_BASE_DIRECTORY = DATA_DIRECTORY / "raw" / "address-base-plus"