"""Parse county name from pipeline filenames."""

import os
import re


def extract_county(filename: str) -> str:
    """Extract the county name from a filename.

    County is everything before the FIPS code (e.g. 'ca001').
    For 'los_angeles_ca037_2024_1.cog' → 'los_angeles'.

    Args:
        filename: Filename or full path (any extension).

    Returns:
        County name string.
    """
    basename = os.path.splitext(os.path.basename(filename))[0]
    parts = basename.split("_")
    for i, part in enumerate(parts):
        if re.match(r'^[a-z]{2}\d{3}$', part):
            return "_".join(parts[:i])
    return parts[0]
