"""Loading AddressBase Plus"""

from pathlib import Path
from zipfile import ZipFile

import pandas as pd

def unzip_all(zip_dir, extract_dir):
    """Extract every .zip in zip_dir into extract_dir
    unless a .csv in exit_dir already exists
    """

    extract_dir.mkdir(parents=True, exist_ok=True)

    zip_paths = sorted(Path(zip_dir).glob("*.zip"))

    for zip_path in zip_paths:
        target = extract_dir / (zip_path.stem)
        if target.exists():
            print(f"Skipping {zip_path.name} (already extracted)")
            continue

        print(f"Extracting {zip_path.name}")
        with ZipFile(zip_path) as zf:
            zf.extractall(target)


# continue from here on

def load_and_append(extract_dir):
    """Read every extracted CSV and concatenate into a single DataFrame.

    Adds a `source_file` column so rows can be traced back to their
    originating file.
    """
    csv_paths = sorted(Path(extract_dir).rglob("*.csv"))
    if not csv_paths:
        raise FileNotFoundError(f"No CSV files found under {extract_dir}")

    frames = []
    for csv_path in csv_paths:
        df = pd.read_csv(csv_path)
        df["source_file"] = csv_path.name
        frames.append(df)

    combined = pd.concat(frames, ignore_index=True)
    print(f"Loaded {len(combined)} rows from {len(csv_paths)} files")
    return combined


def load_addressbase():
    """Full load: unzip if needed, then read and concatenate all CSVs."""
    unzip_all()
    return load_and_append()