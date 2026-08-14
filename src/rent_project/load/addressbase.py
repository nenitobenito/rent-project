"""Loading AddressBase Plus"""

from pathlib import Path
from zipfile import ZipFile

import pandas as pd

# ----------------------------------------
# Loading AddressBase Plus Schema
# ----------------------------------------

def load_schema_new(header_path):
    """Parse a post-2016 (epoch 39+) header file nto column names.
    Define dtypes schema (same for all csv tiles).
    
    Parameters
    -----
    header_path: a path to a csv file with column names.
    """

    columns = pd.read_csv(header_path,header=None,dtype=str).iloc[0].tolist()
    INT_COLUMNS = ['UPRN','UDPRN','PARENT_UPRN','LOCAL_CUSTODIAN_CODE','BUILDING_NUMBER','SAO_START_NUMBER','SAO_END_NUMBER','PAO_START_NUMBER','PAO_END_NUMBER','USRN','OS_ADDRESS_TOID_VERSION','OS_ROADLINK_TOID_VERSION','OS_TOPO_TOID_VERSION','VOA_CT_RECORD','VOA_NDR_RECORD','MULTI_OCC_COUNT']
    FLOAT_COLUMNS = ['X_COORDINATE', 'Y_COORDINATE', 'LATITUDE', 'LONGITUDE']
    DATE_COLUMNS = ['STATE_DATE','LA_START_DATE','LAST_UPDATE_DATE','ENTRY_DATE','RM_START_DATE']
    STRING_COLUMNS = [c for c in columns if c not in INT_COLUMNS + FLOAT_COLUMNS + DATE_COLUMNS]
    DTYPES = {
        **{c: "Int64" for c in INT_COLUMNS},
        **{c: "float64" for c in FLOAT_COLUMNS},
        **{c: "string" for c in STRING_COLUMNS},
    }
    return {"columns" : columns, "dtypes": DTYPES, "date_columns": DATE_COLUMNS}

def load_schema_old(header_path):
    """Parse a pre-2016 (epoch 38-) header file into column names.
    Define dtypes schema (same for all csv tiles).
    
    Parameters
    -----
    header_path: a path to a csv file with column names.
    """

    columns = pd.read_csv(header_path,header=None,dtype=str).iloc[0].tolist()
    INT_COLUMNS = ['UPRN','UDPRN','PARENT_UPRN','LOCAL_CUSTODIAN_CODE','BUILDING_NUMBER','SAO_START_NUMBER','SAO_END_NUMBER','PAO_START_NUMBER','PAO_END_NUMBER','USRN','OS_ADDRESS_TOID_VERSION','OS_ROADLINK_TOID_VERSION','OS_TOPO_TOID_VERSION','VOA_CT_RECORD','VOA_NDR_RECORD','MULTI_OCC_COUNT']
    FLOAT_COLUMNS = ['X_COORDINATE', 'Y_COORDINATE', 'LATITUDE', 'LONGITUDE']
    DATE_COLUMNS = ['STATE_DATE','LA_START_DATE','LAST_UPDATE_DATE','ENTRY_DATE','RM_START_DATE']
    STRING_COLUMNS = [c for c in columns if c not in INT_COLUMNS + FLOAT_COLUMNS + DATE_COLUMNS]
    DTYPES = {
        **{c: "Int64" for c in INT_COLUMNS},
        **{c: "float64" for c in FLOAT_COLUMNS},
        **{c: "string" for c in STRING_COLUMNS},
    }
    return {"columns" : columns, "dtypes": DTYPES, "date_columns": DATE_COLUMNS}

# ----------------------------------------
# Loading AddressBase Plus 2026
# ----------------------------------------

def unzip_all(zip_dir, extract_dir):
    """Extract each .zip in zip_dir into extract_dir
    Skip if a folder in extract_dir already exists

    Parameters
    -----
    zip_dir:     path to a directory with one or more .zip files
    extract_dir: path to target directory (existing or new)
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

def load_tile(schema, file_path):
    """Load a single AddressBase Plus tile CSV.
    Drop addresses outside any of London's 33 local authorities.
    
    Parameters
    -----
    schema:    a dictionary with a pre-parsed schema (same for all csv tiles)
    file_path: path to this specific tile's data CSV
    """

    LONDON_BOROUGHS = ['CITY OF WESTMINSTER','TOWER HAMLETS','WANDSWORTH','CROYDON','BARNET','SOUTHWARK','LAMBETH','EALING','BROMLEY','CAMDEN','BRENT','LEWISHAM','NEWHAM','ENFIELD','GREENWICH','HACKNEY','ISLINGTON','HILLINGDON','HARINGEY','WALTHAM FOREST','HOUNSLOW','HAMMERSMITH AND FULHAM','REDBRIDGE','HAVERING','KENSINGTON AND CHELSEA','BEXLEY','MERTON','HARROW','RICHMOND UPON THAMES','BARKING AND DAGENHAM','SUTTON','KINGSTON UPON THAMES','CITY OF LONDON']

    df = pd.read_csv(
        file_path,header=None,
        names=schema["columns"],dtype=schema["dtypes"],
        parse_dates=schema["date_columns"]
    )
    df = df[df['ADMINISTRATIVE_AREA'].isin(LONDON_BOROUGHS)]
    return df

def load_and_concatenate(header_path, extract_dir):
    """Load all CSVs and concatenate into a single DataFrame.
    
    Parameters
    -----
    header_path: path to a CSV header file, passed into load_schema()
    extract_dir: path to a directory with CSV files to be loaded
    """

    schema = load_schema_new(header_path)
    csv_paths = sorted(Path(extract_dir).rglob("*.csv"))
    print(f"Loading {len(csv_paths)} tiles")
    tiles = [load_tile(schema,p) for p in csv_paths]
    combined = pd.concat(tiles, ignore_index=True)
    print(f"Loaded {len(combined):,} rows from {len(tiles)} tiles.")
    return combined