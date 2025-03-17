import xarray as xr  # Add this line to import xarray
import pandas as pd



data_path = "combined.nc"  # Đường dẫn đến tệp của bạn
data = xr.load_dataset(data_path)
datetime_values = data['datetime'].values
print(data)
datetime_values = data['datetime'].values

# In ra các giá trị datetime trong dữ liệu
print("datasets/source-era5_date-2024-01-01_res-1.0_levels-13_steps-40.nc")
for batch_idx, times in enumerate(datetime_values):
    print(f"Batch {batch_idx}:")
    for time in times:
        print(time)


#
#
#
