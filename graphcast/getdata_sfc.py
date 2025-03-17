import cdsapi

# Initialize the CDS API client
client = cdsapi.Client()

# Define the list of single-level fields to retrieve
single_level_fields = [
    '10m_u_component_of_wind',
    '10m_v_component_of_wind',
    '2m_temperature',
    'geopotential',
    'land_sea_mask',
    'mean_sea_level_pressure',
    'toa_incident_solar_radiation',
    'total_precipitation'
]

# Set up parameters for the data retrieval request
request_params = {
    'product_type': 'reanalysis',
    'variable': single_level_fields,
    'grid': '1.0/1.0',  # 1°x1° spatial resolution
    'year': '2024',
    'month': '01',  # January
    'day': '01',  # 1st of January
    'time': [
        '00:00', '01:00', '02:00', '03:00', '04:00', '05:00', 
        '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00'
    ],
    'format': 'netcdf'
}
dataset = "reanalysis-era5-single-levels"

# Retrieve data and save to a NetCDF file
client.retrieve(
    'reanalysis-era5-single-levels',  # Dataset name
    request_params,                   # Parameters for retrieval
    'single-level.nc'                 # Output file name
)
