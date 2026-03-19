"""Upload metadata artifacts (JSON, STAC, summary CSV) to S3.

Required environment variables:
    METADATA_DIRECTORY  - Local directory containing metadata output
    BUCKET_NAME         - Target S3 bucket
"""

import glob
import os

from src.load.utils.upload_to_s3 import upload_to_s3


def metadata_to_s3():
    """Upload all metadata files from METADATA_DIRECTORY to S3."""
    metadata_dir = os.getenv("METADATA_DIRECTORY", "")
    bucket = os.getenv("BUCKET_NAME", "")
    prefix = "metadata"

    # JSON sidecars
    json_files = sorted(glob.glob(os.path.join(metadata_dir, "json", "*.json")))
    for f in json_files:
        key = f"{prefix}/json/{os.path.basename(f)}"
        upload_to_s3(f, bucket, key)

    # STAC items
    stac_files = sorted(glob.glob(os.path.join(metadata_dir, "stac", "*.stac.json")))
    for f in stac_files:
        key = f"{prefix}/stac/{os.path.basename(f)}"
        upload_to_s3(f, bucket, key)

    # Summary CSV
    csv_path = os.path.join(metadata_dir, "summary.csv")
    has_csv = os.path.isfile(csv_path)
    if has_csv:
        upload_to_s3(csv_path, bucket, f"{prefix}/summary.csv")

    total = len(json_files) + len(stac_files) + (1 if has_csv else 0)
    print(f"Uploaded {total} metadata file(s) to s3://{bucket}/{prefix}/")