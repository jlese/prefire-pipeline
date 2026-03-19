"""Convert step: SID → GeoTIFF → COG → validate.

Required environment variables:
    SID_DIRECTORY      - Directory containing .sid files
    GEOTIFF_DIRECTORY  - Output directory for GeoTIFF files
    COG_DIRECTORY      - Output directory for COG files
    COUNTY_LIST        - Comma-separated list of counties to process
"""

import os

from src.convert.sid_to_geotiff import sid_to_geotiff
from src.convert.geotiff_to_cog import geotiff_to_cog
from src.convert.validate_cogs import validate_cogs
from src.shared.validate_env import validate_env

REQUIRED_ENV_VARS = [
    "SID_DIRECTORY",
    "GEOTIFF_DIRECTORY",
    "COG_DIRECTORY",
    "COUNTY_LIST",
]


def run_convert():
    """Run the full convert pipeline: SID → GeoTIFF → COG → validate."""
    if not validate_env(REQUIRED_ENV_VARS):
        return

    sid_dir = os.getenv("SID_DIRECTORY")
    geotiff_dir = os.getenv("GEOTIFF_DIRECTORY")
    cog_dir = os.getenv("COG_DIRECTORY")
    county_list = os.getenv("COUNTY_LIST")

    print("--- Convert Step ---")

    print("[1/3] Converting SID files to GeoTIFF...")
    sid_to_geotiff(sid_dir, geotiff_dir, county_list)

    print("[2/3] Converting GeoTIFF files to COG...")
    geotiff_to_cog(geotiff_dir, cog_dir)

    print("[3/3] Validating COG files...")
    validate_cogs(cog_dir)

    print("Convert step complete.")