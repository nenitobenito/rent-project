"""Orchestration only"""

from rent_project.config import DATA_DIRECTORY
from rent_project.load.addressbase import unzip_all

def main():
    unzip_all(
        DATA_DIRECTORY / "raw" / "address-base-plus" / "2026" / "compressed",
        DATA_DIRECTORY / "raw" / "address-base-plus" / "2026" / "extracted")

if __name__ == "__main__":
    main()