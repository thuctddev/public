# @title Imports

import dataclasses
import datetime
import functools
import math
import re
from typing import Optional
import haiku as hk
import cartopy.crs as ccrs
from google.cloud import storage
from graphcast import autoregressive
from graphcast import casting
from graphcast import checkpoint
from graphcast import data_utils
from graphcast import graphcast
from graphcast import normalization
from graphcast import rollout
from graphcast import xarray_jax
from graphcast import xarray_tree
from IPython.display import HTML
import ipywidgets as widgets
import haiku as hk
import jax
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import xarray
import xarray as xr  # Add this line to import xarray
import os

# Define the local directory where you want to save the downloaded parameter files
params_directory = "./params"  # Replace with your actual local path
os.makedirs(params_directory, exist_ok=True)

# Initialize Google Cloud Storage client

client = storage.Client.create_anonymous_client()
bucket = client.get_bucket("dm_graphcast")

# List all files in the GCS 'params/' folder and download them
blobs = bucket.list_blobs(prefix="params/")

for blob in blobs:
    # Remove the 'params/' prefix for local file naming
    file_name = blob.name.removeprefix("params/")
    if file_name:  # Skip empty strings
        local_path = os.path.join(params_directory, file_name)
        blob.download_to_filename(local_path)
        print(f"Downloaded {blob.name} to {local_path}")
