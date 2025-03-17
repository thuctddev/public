import xarray as xr
import numpy as np
import pandas as pd

# Load the single-level and pressure-level data
single_level_ds = xr.open_dataset('single-level.nc')
pressure_level_ds = xr.open_dataset('pressure-level.nc')

# Rename dimensions and coordinates to match the target format
single_level_ds = single_level_ds.rename({
    'latitude': 'lat',
    'longitude': 'lon',
    'valid_time': 'time'
})
pressure_level_ds = pressure_level_ds.rename({
    'latitude': 'lat',
    'longitude': 'lon',
    'valid_time': 'time',
    'pressure_level': 'level'
})

# Convert lat and lon coordinates to float32
single_level_ds = single_level_ds.assign_coords(lat=single_level_ds['lat'].astype('float32'), lon=single_level_ds['lon'].astype('float32'))
pressure_level_ds = pressure_level_ds.assign_coords(lat=pressure_level_ds['lat'].astype('float32'), lon=pressure_level_ds['lon'].astype('float32'))

# Sort latitudes in ascending order (-90 to 90)
single_level_ds = single_level_ds.sortby('lat')
pressure_level_ds = pressure_level_ds.sortby('lat')

# Set 'batch' dimension with a single value (1) for both datasets
single_level_ds = single_level_ds.expand_dims('batch', axis=0)
pressure_level_ds = pressure_level_ds.expand_dims('batch', axis=0)

# Ensure that `level` coordinates match the desired format and order levels
pressure_level_ds = pressure_level_ds.assign_coords(level=np.array([50, 100, 150, 200, 250, 300, 400, 500, 600, 700, 850, 925, 1000], dtype=np.int32))

# Adjust variable names for consistency
single_level_ds = single_level_ds.rename({
    'u10': '10m_u_component_of_wind',
    'v10': '10m_v_component_of_wind',
    't2m': '2m_temperature',
    'z': 'geopotential_at_surface',
    'lsm': 'land_sea_mask',
    'msl': 'mean_sea_level_pressure',
    'tisr': 'toa_incident_solar_radiation',
    'tp': 'total_precipitation'
})
pressure_level_ds = pressure_level_ds.rename({
    'u': 'u_component_of_wind',
    'v': 'v_component_of_wind',
    'z': 'geopotential',
    'q': 'specific_humidity',
    't': 'temperature',
    'w': 'vertical_velocity'
})

# Modify land_sea_mask and geopotential_at_surface to only have lat and lon dimensions
single_level_ds['land_sea_mask'] = single_level_ds['land_sea_mask'].isel(batch=0, time=0).squeeze()
single_level_ds['geopotential_at_surface'] = single_level_ds['geopotential_at_surface'].isel(batch=0, time=0).squeeze()

# Select time steps with hour % 6 == 0 and skip the first step if it's not 6 hours from the start
selected_times = single_level_ds.time.sel(time=[t for t in single_level_ds.time.values if pd.Timestamp(t).hour % 6 == 0][1:])
single_level_ds = single_level_ds.sel(time=selected_times)
pressure_level_ds = pressure_level_ds.sel(time=selected_times)

# Accumulate precipitation over each 6-hour interval
precipitation_accumulated = single_level_ds['total_precipitation'].resample(time="6H").sum() #.isel(time=slice(1, None))  # Skip the first sum result
single_level_ds['total_precipitation_6hr'] = precipitation_accumulated
# Remove the variable total_precipitation
# single_level_ds = single_level_ds.drop_vars('total_precipitation')


# Merge the datasets along the time dimension
combined_ds = xr.merge([single_level_ds, pressure_level_ds])

# Generate datetime coordinate for each (batch, time) combination and add to coordinates
datetime_values = pd.to_datetime(selected_times.values)  # Generate datetime based on selected times
datetime_expanded = np.expand_dims(datetime_values, axis=0)  # Expand to match (batch, time) dimensions
combined_ds = combined_ds.assign_coords(datetime=(("batch", "time"), datetime_expanded))

# Save to NetCDF file
combined_ds.to_netcdf("combined_dataset_6h.nc")
