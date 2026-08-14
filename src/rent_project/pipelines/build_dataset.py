"""Orchestration only"""

from rent_project.config import ADDRESS_BASE_DIRECTORY
from rent_project.load.addressbase import load_and_concatenate, unzip_all


def step_build_addressbase2026():
    """Extracts, loads, concatenates, AddressBase Plus tiles (2026).
    Then writes csv.
    Does nothing if the combined CSV already exists.
    """

    output_path = ADDRESS_BASE_DIRECTORY / "2026" / "greater_london_2026_abplus.csv"

    # Check if already exists
    if output_path.exists():
        print("Skiped building 2026 AddressBase Plus (already exists)")
        return output_path

    # Extract zipped tile files
    print("Extracting zip tiles")
    unzip_all(
        ADDRESS_BASE_DIRECTORY/ "2026" / "compressed",
        ADDRESS_BASE_DIRECTORY / "2026" / "extracted"
    )

    # Load and concatenate all tiles (2026)
    print("Loading and concatenating tiles")
    address_base_2026 = load_and_concatenate(
        ADDRESS_BASE_DIRECTORY / "addressbase-plus-post-e-39-header.csv",
        ADDRESS_BASE_DIRECTORY / "2026" / "extracted"
    )

    # Save 2026 Address Base as csv
    print("Writing 2026 AddressBase Plus (csv)")
    address_base_2026.to_csv(output_path,index=False)

# def step_load_addressbase_all_years():
#    """Loads AddressBase Plus 2011, 2021, 2026"""

def main():
    step_build_addressbase2026()
    # step_load_addressbase_all_years
    # step_subset_test_area()
    # step_build_addressbase_history()
    # step_filter_residential()
    # next step goes here

if __name__ == "__main__":
    main()