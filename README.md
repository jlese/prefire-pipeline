# prefire - **California Geospatial Data Lake Pipeline**

This repo is an orchestrator for the scripts used for the **California Geospatial Data Lake Pipeline**

## Convert

### convert.py

Main script for orchestrating convertions between files types ultimately going from MrSID to GeoTIFF to COG.

### sid_to_geotiff.py

Converting MrSID to GeoTIFF

### geotiff_to_cog.py

Converting GeoTIFF to Cloud Optimized GeoTIFF

### validate_cogs.py

Validate whether files are properly created COGs.

## Extract

### extract.py

Main script for orchestrating metadata extraction from cogs. Creates metadata jsons, csv, and STAC's.

### create_metadata.py

Calls helper extractor methods and compiles metadata according to template src\extract\metadata_templates\template.json.

### extract_cog_metadata.py

Pulls COG metadata using GDAL

### extract_raster_metadata.py

Pulls raster metadata using GDAL

## Load

### load.py

Main script for loading metadata and COGs into s3

### cog_to_s3.py

boto3 script for uploading COGs to s3
