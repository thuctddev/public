import xarray as xr
import numpy as np
from pysolar.radiation import get_radiation_direct
from pysolar.solar import get_altitude
import pytz
import datetime
import pandas as pd

# Hàm thêm múi giờ vào datetime
def addTimezone(dt, tz=pytz.UTC):
    if dt.tzinfo is None:
        return tz.localize(dt)
    return dt.astimezone(tz)

# Hàm tính bức xạ mặt trời
def getSolarRadiation(longitude, latitude, dt):
    altitude_degrees = get_altitude(latitude, longitude, addTimezone(dt))
    solar_radiation = get_radiation_direct(dt, altitude_degrees) if altitude_degrees > 0 else 0
    return solar_radiation * 3600  # Đổi đơn vị từ watts sang joules

# Đọc dữ liệu từ file và tính thời gian mới
data_path = "datasets/source-era5_date-2024-01-01_res-1.0_levels-13_steps-01.nc"
data1 = xr.load_dataset(data_path)
datetime_values = data1['time'].values  # Sử dụng 'time' từ data1 làm tham chiếu
last_time = datetime_values[-1]
#new_time = last_time + np.timedelta64(6, 'h')  # Cộng thêm 6h
#new_time = np.datetime64(str(new_time).replace('.000000000',''))
new_time = np.datetime64(last_time + np.timedelta64(6, 'h'), 'ns')




# Tạo dữ liệu SOLAR
lat_range = np.arange(-90, 91, 1)
lon_range = np.arange(0, 360, 1)
dt = np.datetime64(new_time, 's').astype(datetime.datetime)

# # Khởi tạo DataArray để lưu trữ bức xạ mặt trời
# toa_incident_solar_radiation = xr.DataArray(
#     np.zeros((len(lat_range), len(lon_range))),  # Khởi tạo mảng giá trị 0
#     coords=[lat_range, lon_range],
#     dims=["lat", "lon"],
#     name="toa_incident_solar_radiation"  # Tên của biến trong file NetCDF
# )

# # Tính bức xạ mặt trời và lưu vào DataArray
# for i, lat in enumerate(lat_range):
#     for j, lon in enumerate(lon_range):
#         toa_incident_solar_radiation[i, j] = getSolarRadiation(lon, lat, dt)


# # Đóng gói DataArray vào Dataset
# dataset = xr.Dataset({"toa_incident_solar_radiation": toa_incident_solar_radiation})
#dataset.to_netcdf("toa.nc")

dataset = xr.load_dataset("toa.nc")

# Đọc file prediction.nc
data_path = "predictions.nc"
data2 = xr.load_dataset(data_path)
data2 = xr.merge([data2, dataset])

# Chọn các biến cần thiết từ data1 và thêm vào data2
selected_vars = data1[['geopotential_at_surface', 'land_sea_mask']]
data2 = xr.merge([data2, selected_vars])




# Tạo một mảng datetime có kích thước phù hợp cho data2 với giá trị new_time
batch_dim = data2.dims.get("batch", 1)
time_dim = data2.dims["time"]
datetime_values_new = np.full((batch_dim, time_dim), new_time, dtype="datetime64[ns]")


# Gán mảng datetime mới vào Dataset data2
data2 = data2.assign_coords(datetime=(["batch", "time"], datetime_values_new))

# Sử dụng thời gian từ data1 để tạo biến datetime cho data2
datetime_values = np.expand_dims(datetime_values, axis=0)  # Điều chỉnh cho phù hợp với kích thước batch


data1.to_netcdf("file1.nc")
data2.to_netcdf("file2.nc")
ds1 = xr.open_dataset('file1.nc')
ds2 = xr.open_dataset('file2.nc')
time1 = ds1.time
time2 = ds2.time

# Lấy thời gian cuối cùng trong ds1 và tạo chuỗi thời gian mới cho ds2 với khoảng cách 6 giờ
last_time_file1 = ds1.time[-1].values
num_time_steps_file2 = ds2.dims['time']
adjusted_times = np.array([np.datetime64(last_time_file1) + np.timedelta64(6 * i, 'h') for i in range(1, num_time_steps_file2 + 1)], dtype="datetime64[ns]")

# Gán chuỗi thời gian mới cho cả `time` và `datetime` trong `ds2`
ds2 = ds2.assign_coords(time=("time", adjusted_times))
ds2 = ds2.assign_coords(datetime=("time", adjusted_times))

# Điều chỉnh `toa_incident_solar_radiation` để khớp với các bước thời gian mới
solar_radiation_data = np.expand_dims(ds2['toa_incident_solar_radiation'].values, axis=0)
solar_radiation_data = np.repeat(solar_radiation_data, num_time_steps_file2, axis=0)  # Lặp lại cho mỗi bước thời gian

# Tạo lại `toa_incident_solar_radiation` với chiều `time` đã điều chỉnh
toa_incident_solar_radiation = xr.DataArray(
    solar_radiation_data,
    coords={"time": adjusted_times, "lat": ds2.lat, "lon": ds2.lon},
    dims=["time", "lat", "lon"],
    name="toa_incident_solar_radiation"
)

# Gán biến `toa_incident_solar_radiation` mới vào `ds2`
ds2["toa_incident_solar_radiation"] = toa_incident_solar_radiation

combined = xr.merge([ds1, ds2])

combined.to_netcdf('combined.nc')