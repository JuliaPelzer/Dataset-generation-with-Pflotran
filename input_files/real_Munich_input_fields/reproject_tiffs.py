import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

# reproject all tiffs to correct crs

def reproject_tiff(src_path, dst_path, dst_crs="EPSG:25832"):
    with rasterio.open(src_path) as src:
        transform, width, height = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds)
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
    
folder_path = "input_files/real_Munich_input_fields/"
datas_name = ["Hydraulic_conductivity_20m_resolution", "Drawdown_20m_resolution"]
for data_name in datas_name:
    reproject_tiff(f"{folder_path}originals/{data_name}.tif", f"{folder_path}epsg_25832/{data_name}.tif")
