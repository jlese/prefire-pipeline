"""Extract COG-specific metadata (layout, block size, compression, overviews) via GDAL."""

from __future__ import annotations

from osgeo import gdal

gdal.UseExceptions()


def extract_cog_metadata(cog_path: str) -> dict:
    """Return COG structure metadata for *cog_path*.

    Args:
        cog_path: Path to a COG file.

    Returns:
        Dict with keys: is_cog, layout, blocksize, compression,
        interleave, overview_resampling, overview_levels.
    """
    ds = gdal.Open(cog_path, gdal.GA_ReadOnly)
    if ds is None:
        raise IOError(f"GDAL could not open: {cog_path}")

    img_struct = ds.GetMetadata("IMAGE_STRUCTURE") or {}

    layout = img_struct.get("LAYOUT")
    is_cog = layout == "COG"
    compression = img_struct.get("COMPRESSION")
    interleave = img_struct.get("INTERLEAVE")
    overview_resampling = img_struct.get("OVERVIEW_RESAMPLING")

    band1 = ds.GetRasterBand(1)
    block_x, block_y = band1.GetBlockSize()

    overview_levels = [
        [band1.GetOverview(i).XSize, band1.GetOverview(i).YSize]
        for i in range(band1.GetOverviewCount())
    ]

    ds = None  # close dataset

    return {
        "is_cog": is_cog,
        "layout": layout,
        "blocksize": {"x": block_x, "y": block_y},
        "compression": compression,
        "interleave": interleave,
        "overview_resampling": overview_resampling,
        "overview_levels": overview_levels,
    }
