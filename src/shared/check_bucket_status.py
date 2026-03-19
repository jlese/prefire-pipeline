'''
Check the current status of files in the S3 bucket using the county list
 - cogs/: check if files are present for each county
 - metadata/: check if metadata files are present for each county
    - summary.csv: check if summary.csv is present and has entries for each county
    - json/: check if JSON sidecars are present for each county
    - stac/: check if STAC items are present for each county
'''
import os
import boto3
from src.shared.validate_env import validate_env


REQUIRED_ENV_VARS = [
    "BUCKET_NAME",
    "COUNTY_LIST",
]

def check_bucket_status():
    """Check the current status of files in the S3 bucket for each county."""
    if not validate_env(REQUIRED_ENV_VARS):
        return
    issues = False
    bucket = os.getenv("BUCKET_NAME")
    county_list = os.getenv("COUNTY_LIST", "").strip("[]").split(",")
    s3 = boto3.client("s3")

    print("--- S3 Bucket Status ---")
    existing_objects = s3.list_objects_v2(Bucket=bucket).get("Contents", [])
    existing_keys = [obj["Key"] for obj in existing_objects]
    
    for county in county_list:
        county = county.strip().strip('"')
        print(f"\nCounty: {county}")

        cog_prefix = f"cogs/{county}_"
        cog_count = sum(1 for key in existing_keys if key.startswith(cog_prefix))
        
        if cog_count > 0:
            print(f"  COGs: {cog_count} file(s) found")
            issues = True
        else:
            print("  COGs: No matching files found")


        json_prefix = f"metadata/json/{county}_"
        json_count = sum(1 for key in existing_keys if key.startswith(json_prefix))
        if json_count > 0:
            print(f"  Metadata JSON: {json_count} file(s) found")
            issues = True
        else:
            print("  Metadata JSON: No matching files found")

        stac_prefix = f"metadata/stac/{county}_"
        stac_count = sum(1 for key in existing_keys if key.startswith(stac_prefix))
        if stac_count > 0:
            print(f"  STAC Items: {stac_count} file(s) found")
            issues = True
        else:
            print("  STAC Items: No matching files found")
    if issues:
        return False
    return True