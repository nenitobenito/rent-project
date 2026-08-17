"""Orchestration only"""

from rent_project.config import (
    ADDRESS_BASE_INTERIM_DIRECTORY,
    ADDRESS_BASE_RAW_DIRECTORY,
)
from rent_project.load.addressbase import (
    load_and_concatenate,
    load_schema_new,
    load_schema_old,
    unzip_all,
)


def step_build_addressbase2026():
    """Extracts, loads, concatenates, AddressBase Plus tiles (2026).
    Then writes csv.
    Does nothing if the combined CSV already exists.
    """

    output_path = ADDRESS_BASE_RAW_DIRECTORY / "2026" / "greater_london_2026_abplus.csv"

    # Check if already exists
    if output_path.exists():
        print("Skiped building 2026 AddressBase Plus (already exists)")
        return

    # Extract zipped tile files
    print("Extracting zip tiles")
    unzip_all(
        ADDRESS_BASE_RAW_DIRECTORY/ "2026" / "compressed",
        ADDRESS_BASE_RAW_DIRECTORY / "2026" / "extracted"
    )

    # Load and concatenate all tiles (2026)
    print("Loading and concatenating tiles")
    schema_new = load_schema_new(ADDRESS_BASE_RAW_DIRECTORY / "addressbase-plus-post-e-39-header.csv")
    address_base_2026 = load_and_concatenate(
        schema_new,
        ADDRESS_BASE_RAW_DIRECTORY / "2026" / "extracted"
    )

    # Save 2026 Address Base as csv
    print("Writing 2026 AddressBase Plus (csv)")
    address_base_2026.to_csv(output_path,index=False)


#def step_clip_addressbase_all_years():
#    """Loads and clips AddressBase Plus 2011, 2021, 2026 to Greater London.
#    Then writes csv.
#    Does nothing if the combined CSV already exists.
#    """

#    schema_old = load_schema_old(ADDRESS_BASE_RAW_DIRECTORY / "addressbase-plus-pre-e-39-header.csv")
#    schema_new = load_schema_new(ADDRESS_BASE_RAW_DIRECTORY / "addressbase-plus-post-e-39-header.csv")

#    # 2011
#    output_path = ADDRESS_BASE_INTERIM_DIRECTORY / "greater_london_2011_abplus_clipped.csv"
#    if output_path.exists():
#        print("Skiped clipping 2011 AddressBase Plus (already exists)")
#        return
#    print("Loading 2021 AddressBase Plus")

#   # 2021
#    output_path = ADDRESS_BASE_INTERIM_DIRECTORY / "greater_london_2021_abplus_clipped.csv"
#    if output_path.exists():
#        print("Skiped clipping 2021 AddressBase Plus (already exists)")
#        return

#    # 2026
#    output_path = ADDRESS_BASE_INTERIM_DIRECTORY / "greater_london_2026_abplus_clipped.csv"
#    if output_path.exists():
#        print("Skiped clipping 2026 AddressBase Plus (already exists)")
#        return

def main():
    step_build_addressbase2026()
    # step_clip_addressbase_all_years()
    # step_load_addressbase_all_years()
    # step_subset_test_area()
    # step_build_addressbase_history()
    # step_filter_residential()
    # next step goes here

if __name__ == "__main__":
    main()