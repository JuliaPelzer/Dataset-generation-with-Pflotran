import pathlib
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

# reproject all tiffs to correct crs

def reproject_tiff(src_path, dst_path, dst_crs="EPSG:25832"):
    with rasterio.open(src_path) as src:
        transform, width, height = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds)
        print(src.crs, dst_crs, src.width, src.height, src.bounds)
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': dst_crs,
            'transform': transform,
            'width': width,
            'height': height
        })

        with rasterio.open(dst_path, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.nearest)
    
if __name__ == "__main__":
    # reproject_tiff("data/originals/Hydraulic_conductivity_20m_resolution.tif", "data/epsg_25832/Hydraulic_conductivity_20m_resolution.tif")
    # reproject_tiff("data/originals/Drawdown_20m_resolution.tif", "data/epsg_25832/Drawdown_20m_resolution.tif")

    folder = pathlib.Path("input_files/real_Munich_input_fields/originals/")
    for file in folder.iterdir():
        if file.suffix == ".tif":
            reproject_tiff(file, f"input_files/real_Munich_input_fields/epsg_25832/{file.name}")