"""Extract step: build metadata, STAC items, and summary CSV for each COG.

Checks S3 for an existing summary.csv — if found, downloads it so new rows
are appended rather than overwriting.

Required environment variables:
    COG_DIRECTORY       - Directory containing .cog files
    METADATA_DIRECTORY  - Local output directory for metadata
    BUCKET_NAME         - S3 bucket (used to check for existing summary.csv)
    STAC_COLLECTION     - STAC collection ID
"""

from __future__ import annotations

import glob
import os
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

from src.extract.create_metadata import build_metadata, write_metadata_json, append_metadata_csv
from src.extract.create_stac import build_stac_item, write_stac_item
from src.shared.validate_env import validate_env

REQUIRED_ENV_VARS = [
    "COG_DIRECTORY",
    "METADATA_DIRECTORY",
    "BUCKET_NAME",
    "STAC_COLLECTION",
]


def run_extract(cog_uris: dict[str, dict] | None = None) -> list[dict]:
    """Build metadata, JSON sidecars, STAC items, and summary CSV for all COGs.

    Args:
        cog_uris: Optional map of COG filename → {"s3_uri": ..., "etag": ...}
                  returned by the load step. When None, URIs are left blank.

    Returns:
        List of metadata dicts, one per processed COG.
    """
    if not validate_env(REQUIRED_ENV_VARS):
        return []

    cog_dir = os.getenv("COG_DIRECTORY")
    output_dir = os.getenv("METADATA_DIRECTORY")
    bucket = os.getenv("BUCKET_NAME")
    collection = os.getenv("STAC_COLLECTION")
    cog_uris = cog_uris or {}

    # Download existing summary.csv from S3 so we append instead of overwrite
    csv_path = os.path.join(output_dir, "summary.csv")
    _sync_summary_csv_from_s3(bucket, csv_path)

    cogs = sorted(glob.glob(os.path.join(cog_dir, "*.cog")))
    if not cogs:
        print(f"No *.cog files found in: {cog_dir}")
        return []

    print("--- Extract Step ---")
    print(f"Processing {len(cogs)} COG(s) → {output_dir}")
    results: list[dict] = []

    for i, cog_path in enumerate(cogs, 1):
        fname = os.path.basename(cog_path)
        print(f"[{i}/{len(cogs)}] {fname}")
        uri_info = cog_uris.get(fname, {})
        try:
            metadata = _extract_single_cog(cog_path, output_dir, uri_info, collection)
            results.append(metadata)
        except Exception as e:
            print(f"  ERROR processing {fname}: {e}")

    print(f"Extract step complete. {len(results)}/{len(cogs)} COG(s) processed.")
    return results


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _extract_single_cog(
    cog_path: str,
    output_dir: str,
    uri_info: dict,
    collection: str | None,
) -> dict:
    """Build metadata, JSON sidecar, STAC item, and CSV row for one COG."""
    stem = Path(cog_path).stem

    metadata = build_metadata(
        cog_path,
        s3_uri=uri_info.get("s3_uri"),
        etag=uri_info.get("etag"),
        collection=collection,
        compute_checksum=False,
    )

    json_path = os.path.join(output_dir, "json", f"{stem}.json")
    stac_path = os.path.join(output_dir, "stac", f"{stem}.stac.json")
    csv_path = os.path.join(output_dir, "summary.csv")

    metadata["stac"]["item_path"] = stac_path

    write_metadata_json(metadata, json_path)
    append_metadata_csv(metadata, csv_path)
    write_stac_item(build_stac_item(metadata), stac_path)

    return metadata


def _sync_summary_csv_from_s3(bucket: str, local_csv_path: str) -> None:
    """Download summary.csv from S3 if it exists, so new rows are appended."""
    s3_key = "metadata/summary.csv"
    try:
        s3 = boto3.client("s3")
        s3.head_object(Bucket=bucket, Key=s3_key)
        os.makedirs(os.path.dirname(local_csv_path), exist_ok=True)
        s3.download_file(bucket, s3_key, local_csv_path)
        print(f"Found existing summary.csv in s3://{bucket}/{s3_key}, will append.")
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            print("No existing summary.csv in S3, creating new.")
        else:
            print(f"Warning: could not check S3 for summary.csv: {e}")
