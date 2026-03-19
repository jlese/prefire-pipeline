import os

def check_if_county_files_exist(county: str, directory: str) -> bool:
    """Check if files for a given county exist in the specified directory.

    Args:
        county: Name of the county to check for (e.g., "Los_Angeles").
        directory: Directory to check for files (e.g., "cogs/").

    Returns:
        True if files exist for the county, False otherwise.
    """
    prefix = f"{county}_"
    return any(filename.startswith(prefix) for filename in os.listdir(directory))