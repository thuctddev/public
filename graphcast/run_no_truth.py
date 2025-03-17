import xarray as xr
import pandas as pd
import numpy as np
ds1 = xr.open_dataset('file1.nc')
ds2 = xr.open_dataset('file2.nc')
# Lấy các giá trị time từ mỗi dataset
time1 = ds1.time
time2 = ds2.time

adjusted_time = np.datetime64(ds1.time[-1].values) + np.timedelta64(6, 'h')

# Cập nhật time của ds2
ds2 = ds2.assign_coords(time=[adjusted_time])
ds2['toa_incident_solar_radiation'] = ds2['toa_incident_solar_radiation'].expand_dims(time=[adjusted_time])
# Hợp nhất hai file theo biến thời gian
combined = xr.merge([ds1, ds2])
print(combined)
combined.to_netcdf('combined.nc')