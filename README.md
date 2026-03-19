# prefire - **California Geospatial Data Lake Pipeline**

Pipeline for converting MrSID imagery to Cloud-Optimized GeoTIFFs, extracting metadata, and loading everything into S3.

## Usage

```bash
python -m src.main [convert|load|extract|all]
```

| Command   | Description |
|-----------|-------------|
| `convert` | SID → GeoTIFF → COG → validate |
| `load`    | Upload COGs to S3 → extract metadata → upload metadata to S3 |
| `extract` | Build metadata / STAC / CSV for local COGs (standalone) |
| `all`     | Run `convert` then `load` (default) |

## Pipeline Flow

```
convert ──→ load
              ├─ [1] Upload COGs to S3
              ├─ [2] Extract metadata (using S3 URIs)
              └─ [3] Upload metadata to S3
```

The load step calls extract internally after COGs are uploaded, so the extracted metadata contains the correct S3 URIs and ETags.

The extract step checks S3 for an existing `summary.csv`. If found it downloads and appends to it; otherwise it creates a new one.

## Environment Variables

All variables are loaded from a `.env` file via `python-dotenv`.

| Variable | Required By | Description |
|----------|-------------|-------------|
| `SID_DIRECTORY` | convert | Directory containing `.sid` source files |
| `GEOTIFF_DIRECTORY` | convert | Output directory for GeoTIFF files |
| `COG_DIRECTORY` | convert, load, extract | Directory for COG files (output of convert, input to load/extract) |
| `COUNTY_LIST` | convert | Comma-separated list of counties to process |
| `BUCKET_NAME` | load, extract | Target S3 bucket name |
| `STAC_COLLECTION` | load, extract | STAC collection ID used in metadata |
| `METADATA_DIRECTORY` | load, extract | Local directory for metadata output (JSON, STAC, CSV) |

## Project Structure

```
src/
├── main.py                  # Entry point, argument parsing
├── convert/
│   ├── convert.py           # Convert orchestrator
│   ├── sid_to_geotiff.py    # MrSID → GeoTIFF (mrsidgeodecode)
│   ├── geotiff_to_cog.py    # GeoTIFF → COG (GDAL)
│   └── validate_cogs.py     # Validate COG files (rio cogeo)
├── extract/
│   ├── extract.py           # Extract orchestrator
│   ├── create_metadata.py   # Build metadata dict, write JSON/CSV
│   ├── create_stac.py       # Build STAC item from metadata
│   ├── extract_cog_metadata.py    # COG-specific metadata (GDAL)
│   ├── extract_raster_metadata.py # Raster/spatial metadata (GDAL)
│   └── metadata_templates/
│       └── template.json    # Metadata JSON template
├── load/
│   ├── load.py              # Load orchestrator
│   ├── cog_to_s3.py         # Upload COGs to S3
│   ├── metadata_to_s3.py    # Upload metadata to S3
│   └── utils/
│       └── upload_to_s3.py  # Generic S3 upload helper
└── shared/
    ├── validate_env.py      # Environment variable validation
    └── print_progress_bar.py # CLI progress bar
```
