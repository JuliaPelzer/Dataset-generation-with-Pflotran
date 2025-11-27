import yaml
from pathlib import Path
import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.warp import reproject, Resampling as WarpResampling

def main(src_dir:Path, dst_dir:Path, resolution:int = 20):
    # Configuration
    dst_dir.mkdir(parents=True, exist_ok=True)
    res_file = dst_dir / "resolution.yaml"
    with open(res_file, 'w') as f:
        yaml.dump([resolution], f)

    print("Processing rasters...")

    # 1. Load and Aggregate 'fl' (Flur_20.tif)
    fl_path = src_dir / "Flur_20.tif"
    with rasterio.open(fl_path) as src:
        data = src.read(1)
        profile = src.profile.copy()
        transform = src.transform
        
        # Calculate new dimensions
        height, width = data.shape
        new_height = height // 2
        new_width = width // 2
        
        # Crop to ensure divisibility by 2 (equivalent to expand=FALSE)
        data_cropped = data[:new_height*2, :new_width*2]
        
        # Reshape to (new_h, 2, new_w, 2) to calculate median over blocks
        reshaped = data_cropped.reshape(new_height, 2, new_width, 2)
        
        # Calculate median, ignoring NaNs (na.rm=TRUE)
        fl_data = np.nanmedian(reshaped, axis=(1, 3))
        
        # Update transform for the new resolution (2x larger pixels)
        new_transform = transform * transform.scale(2, 2)
        
        # Update profile
        profile.update({
            'height': new_height,
            'width': new_width,
            'transform': new_transform,
            'dtype': 'float32'  # Ensure float for NaNs
        })
        print(new_transform)

        fl_profile = profile
        fl_transform = new_transform
        fl_crs = src.crs

    print("Aggregated Flur_20.tif")

    # 2. Resample other rasters to match 'fl'
    files_to_resample = {
        "c": "Cond_20.tif",
        "dir": "darcydir_south_zero.tif",
        "dd": "Drawdown_20.tif",
        "g": "Grad_20.tif",
        "gw": "Gwgl_20.tif",
        "t": "Thick_20.tif",
        "tok": "Tok_20.tif",
        "dir2": "Direc_20.tif"  # Not used later, but included for completeness
    }
    
    resampled_data = {}
    
    for key, filename in files_to_resample.items():
        with rasterio.open(src_dir / filename) as src:
            destination = np.zeros((fl_profile['height'], fl_profile['width']), dtype=np.float32)
            
            reproject(
                source=rasterio.band(src, 1),
                destination=destination,
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=fl_transform,
                dst_crs=fl_crs,
                resampling=WarpResampling.bilinear
            )
            
            # Handle nodata if present in source, though we are using float32 destination
            # If source had specific nodata, reproject handles it.
            
            resampled_data[key] = destination
            print(f"Resampled {filename}")

    # 3. Adjust values
    
    t_data = resampled_data['t']
    # Create mask where t is NaN
    t_nan_mask = np.isnan(t_data)
    
    # Apply mask to fl
    fl_data[t_nan_mask] = np.nan
    fl_data[fl_data <= 0] = 0
    
    # Apply mask to others
    keys_to_mask = ['c', 'g', 'gw', 'tok', 'dd', 'dir', 'dir2', 't']
    for key in keys_to_mask:
        resampled_data[key][t_nan_mask] = np.nan

    # 4. Write rasters
    output_mapping = {
        "g": "Grad_20.tif",
        "c": "Cond_20.tif",
        "t": "Thick_20.tif",
        "fl": "Flur_20.tif",
        "dd": "Drawdown_20.tif",
        "dir": "darcydir_south_zero.tif",
        "dir2": "Direc_20.tif",
        "gw": "Gwgl_20.tif",
        "tok": "Tok_20.tif"
    }
    
    # Add fl to resampled_data for writing
    resampled_data['fl'] = fl_data
    
    print("Writing output files...")
    
    for key, out_filename in output_mapping.items():
        out_path = dst_dir / out_filename
        data_to_write = resampled_data[key]
        
        # Ensure we write with the correct profile
        # We might need to update nodata value if it wasn't set
        out_profile = fl_profile.copy()
        if out_profile.get('nodata') is None:
             out_profile['nodata'] = np.nan
             
        with rasterio.open(out_path, 'w', **out_profile) as dst:
            dst.write(data_to_write, 1)
        
        print(f"Written {out_filename}")

if __name__ == "__main__":
    
    src_dir = Path("shared_data_Fabian")
    dst_dir = Path("aggregated")
    orig_res = 20
    main(
        src_dir,
        dst_dir,
        orig_res
    )