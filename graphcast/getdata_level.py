import cdsapi

# Initialize the CDS API client
client = cdsapi.Client()

# Define the list of pressure-level fields to retrieve
pressure_level_fields = [
    'u_component_of_wind',
    'v_component_of_wind',
    'geopotential',
    'specific_humidity',
    'temperature',
    'vertical_velocity'
]

# Define the pressure levels to retrieve, converted to strings for compatibility
pressure_levels = [str(level) for level in [50, 100, 150, 200, 250, 300, 400, 500, 600, 700, 850, 925, 1000]]

# Set up parameters for the data retrieval request
request_params = {
    'product_type': 'reanalysis',
    'variable': pressure_level_fields,
    'grid': '1.0/1.0',  # 1°x1° spatial resolution
    'year': '2024',
    'month': '01',      # January
    'day': '01',        # 1st of January
    'time': ['06:00', '12:00','18:00'],  # Times to retrieve
    'pressure_level': pressure_levels,  # Pressure levels in hPa
    'format': 'netcdf'
}

# Retrieve data and save to a NetCDF file
client.retrieve(
    'reanalysis-era5-pressure-levels',  # Dataset name
    request_params,                     # Parameters for retrieval
    'pressure-level.nc'                 # Output file name
)
