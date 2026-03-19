"""Convert MrSID (.sid) files to GeoTIFF (.tif) using mrsidgeodecode."""

import glob
import os
import subprocess

from src.shared.check_if_file_exists import check_if_county_files_exist
from src.shared.parse_county import extract_county
from src.shared.print_progress_bar import print_progress_bar


def sid_to_geotiff(sid_directory: str, geotiff_directory: str, county_list: str) -> None:
    """Decode MrSID files to GeoTIFF for counties in county_list.

    Args:
        sid_directory:    Directory containing .sid files.
        geotiff_directory: Output directory for .tif files.
        county_list:      Comma-separated county names to include.
    """
    all_sid_files = glob.glob(os.path.join(sid_directory, "*.sid"))
    sid_files = [f for f in all_sid_files if extract_county(f) in county_list]
    total = len(sid_files)
    print_progress_bar(0, total, prefix='Progress:', suffix='Complete', length=50)

    for i, filename in enumerate(sid_files, start=1):
        county = extract_county(filename)
        if check_if_county_files_exist(county, geotiff_directory):
            print(f"  GeoTIFFs for {county} already exist. Skipping.")
            continue

        print(f"\nProcessing {filename}...")
        geotiff_filename = os.path.join(
            geotiff_directory,
            os.path.basename(filename).replace(".sid", ".tif"),
        )
        subprocess.run(["mrsidgeodecode", "-i", filename, "-o", geotiff_filename])
        print(f"Converted {filename} to {geotiff_filename}")
        print_progress_bar(i, total, prefix='Progress:', suffix='Complete', length=50)

    print("All files processed (MrSID -> GeoTIFF).")