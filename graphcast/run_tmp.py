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

def parse_file_parts(file_name):
  return dict(part.split("-", 1) for part in file_name.split("_"))

# @title Authenticate with Google Cloud Storage

gcs_client = storage.Client.create_anonymous_client()
gcs_bucket = gcs_client.get_bucket("dm_graphcast")

# @title Plotting functions

def select(
    data: xarray.Dataset,
    variable: str,
    level: Optional[int] = None,
    max_steps: Optional[int] = None
    ) -> xarray.Dataset:
  data = data[variable]
  if "batch" in data.dims:
    data = data.isel(batch=0)
  if max_steps is not None and "time" in data.sizes and max_steps < data.sizes["time"]:
    data = data.isel(time=range(0, max_steps))
  if level is not None and "level" in data.coords:
    data = data.sel(level=level)
  return data

def scale(
    data: xarray.Dataset,
    center: Optional[float] = None,
    robust: bool = False,
    ) -> tuple[xarray.Dataset, matplotlib.colors.Normalize, str]:
  vmin = np.nanpercentile(data, (2 if robust else 0))
  vmax = np.nanpercentile(data, (98 if robust else 100))
  if center is not None:
    diff = max(vmax - center, center - vmin)
    vmin = center - diff
    vmax = center + diff
  return (data, matplotlib.colors.Normalize(vmin, vmax),
          ("RdBu_r" if center is not None else "viridis"))

def plot_data(
    data: dict[str, xarray.Dataset],
    fig_title: str,
    plot_size: float = 5,
    robust: bool = False,
    cols: int = 4
    ) -> tuple[xarray.Dataset, matplotlib.colors.Normalize, str]:

  first_data = next(iter(data.values()))[0]
  max_steps = first_data.sizes.get("time", 1)
  assert all(max_steps == d.sizes.get("time", 1) for d, _, _ in data.values())

  cols = min(cols, len(data))
  rows = math.ceil(len(data) / cols)
  figure = plt.figure(figsize=(plot_size * 2 * cols,
                               plot_size * rows))
  figure.suptitle(fig_title, fontsize=16)
  figure.subplots_adjust(wspace=0, hspace=0)
  figure.tight_layout()

  images = []
  for i, (title, (plot_data, norm, cmap)) in enumerate(data.items()):
    ax = figure.add_subplot(rows, cols, i+1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title)
    im = ax.imshow(
        plot_data.isel(time=0, missing_dims="ignore"), norm=norm,
        origin="lower", cmap=cmap)
    plt.colorbar(
        mappable=im,
        ax=ax,
        orientation="vertical",
        pad=0.02,
        aspect=16,
        shrink=0.75,
        cmap=cmap,
        extend=("both" if robust else "neither"))
    images.append(im)

  def update(frame):
    if "time" in first_data.dims:
      td = datetime.timedelta(microseconds=first_data["time"][frame].item() / 1000)
      figure.suptitle(f"{fig_title}, {td}", fontsize=16)
    else:
      figure.suptitle(fig_title, fontsize=16)
    for im, (plot_data, norm, cmap) in zip(images, data.values()):
      im.set_data(plot_data.isel(time=frame, missing_dims="ignore"))

  ani = animation.FuncAnimation(
      fig=figure, func=update, frames=max_steps, interval=250)
  plt.close(figure.number)
  return HTML(ani.to_jshtml())


# @title Choose the model
# Define the local directory for parameter files
params_directory = "./params"  # Replace with the actual local path

# List all parameter files in the local params directory
params_file_options = [
    name for name in os.listdir(params_directory)
    if name.endswith(".nc")  # Adjust extension as needed
]

# Create sliders and dropdowns for model configuration
random_mesh_size = widgets.IntSlider(value=4, min=4, max=6, description="Mesh size:")
random_gnn_msg_steps = widgets.IntSlider(value=4, min=1, max=32, description="GNN message steps:")
random_latent_size = widgets.Dropdown(options=[int(2**i) for i in range(4, 10)], value=32, description="Latent size:")
random_levels = widgets.Dropdown(options=[13, 37], value=13, description="Pressure levels:")

# Dropdown for selecting the parameter file
params_file = widgets.Dropdown(
    options=params_file_options,
    description="Params file:",
    layout={"width": "max-content"}
)

# Create tabs for selecting either random configuration or loading from checkpoint
source_tab = widgets.Tab([
    widgets.VBox([
        random_mesh_size,
        random_gnn_msg_steps,
        random_latent_size,
        random_levels,
    ]),
    params_file,
])
source_tab.set_title(0, "Random")
source_tab.set_title(1, "Checkpoint")
widgets.VBox([
    source_tab,
    widgets.Label(value="Run the next cell to load the model. Rerunning this cell clears your selection.")
])

# Determine the source of the configuration: Random or Checkpoint
source = source_tab.get_title(source_tab.selected_index)

if source == "Random":
    # Configuration from random settings
    params = None  # Filled in below
    state = {}
    model_config = graphcast.ModelConfig(
        resolution=0,
        mesh_size=random_mesh_size.value,
        latent_size=random_latent_size.value,
        gnn_msg_steps=random_gnn_msg_steps.value,
        hidden_layers=1,
        radius_query_fraction_edge_length=0.6
    )
    task_config = graphcast.TaskConfig(
        input_variables=graphcast.TASK.input_variables,
        target_variables=graphcast.TASK.target_variables,
        forcing_variables=graphcast.TASK.forcing_variables,
        pressure_levels=graphcast.PRESSURE_LEVELS[random_levels.value],
        input_duration=graphcast.TASK.input_duration,
    )
else:
    assert source == "Checkpoint"
    # Load parameters from the local file system
    params_path = os.path.join(params_directory, params_file.value)
    with open(params_path, "rb") as f:
        ckpt = checkpoint.load(f, graphcast.CheckPoint)
    
    params = ckpt.params
    state = {}
    model_config = ckpt.model_config
    task_config = ckpt.task_config

    # Print checkpoint metadata
    print("Model description:\n", ckpt.description, "\n")
    print("Model license:\n", ckpt.license, "\n")

# Display the model configuration for verification
print(model_config)


# @title Get and filter the list of available example datasets

# dataset_file_options = [
#     name for blob in gcs_bucket.list_blobs(prefix="dataset/")
#     if (name := blob.name.removeprefix("dataset/"))]  # Drop empty string.

# def data_valid_for_model(
#     file_name: str, model_config: graphcast.ModelConfig, task_config: graphcast.TaskConfig):
#   file_parts = parse_file_parts(file_name.removesuffix(".nc"))
#   return (
#       model_config.resolution in (0, float(file_parts["res"])) and
#       len(task_config.pressure_levels) == int(file_parts["levels"]) and
#       (
#           ("total_precipitation_6hr" in task_config.input_variables and
#            file_parts["source"] in ("era5", "fake")) or
#           ("total_precipitation_6hr" not in task_config.input_variables and
#            file_parts["source"] in ("hres", "fake"))
#       )
#   )
# import os
# def download_valid_datasets(model_config, task_config, download_path="datasets"):
#     # Ensure the download directory exists
#     os.makedirs(download_path, exist_ok=True)

#     # Filter and download each valid dataset
#     for file_name in dataset_file_options:
#         if data_valid_for_model(file_name, model_config, task_config):
#             blob = gcs_bucket.blob(f"dataset/{file_name}")
#             download_destination = os.path.join(download_path, file_name)
#             blob.download_to_filename(download_destination)
#             print(f"Downloaded: {file_name}")

#download_valid_datasets(model_config, task_config)
#exit()

# dataset_file = widgets.Dropdown(
#     options=[
#         (", ".join([f"{k}: {v}" for k, v in parse_file_parts(option.removesuffix(".nc")).items()]), option)
#         for option in dataset_file_options
#         if data_valid_for_model(option, model_config, task_config)
#     ],
#     description="Dataset file:",
#     layout={"width": "max-content"})
# widgets.VBox([
#     dataset_file,
#     widgets.Label(value="Run the next cell to load the dataset. Rerunning this cell clears your selection and refilters the datasets that match your model.")
# ])

# print(dataset_file)
# @title Load weather data

# if not data_valid_for_model(dataset_file.value, model_config, task_config):
#   raise ValueError(
#       "Invalid dataset file, rerun the cell above and choose a valid dataset file.")

# with gcs_bucket.blob(f"dataset/{dataset_file.value}").open("rb") as f:
#   example_batch = xarray.load_dataset(f).compute()

# assert example_batch.dims["time"] >= 3  # 2 for input, >=1 for targets

# print(", ".join([f"{k}: {v}" for k, v in parse_file_parts(dataset_file.value.removesuffix(".nc")).items()]))

# print(example_batch)

# @title Choose data to plot

import os

# Define the local directory where the datasets are stored
dataset_directory = "./datasets"  # Replace with your local path

# List all files in the local dataset directory
dataset_file_options = [
    name for name in os.listdir(dataset_directory)
    if name.endswith(".nc")
]
import re
def parse_file_parts(file_name):
    # Remove ".nc" suffix and split by underscores
    file_name = file_name.removesuffix(".nc")
    
    # Define a regex to extract parts
    pattern = r"source-(?P<source>[^_]+)_date-(?P<date>[^_]+)_res-(?P<res>[^_]+)_levels-(?P<levels>[^_]+)_steps-(?P<steps>[^_]+)"
    match = re.match(pattern, file_name)
    
    # Return dictionary if match found; otherwise, None
    if match:
        return match.groupdict()
    else:
        print(f"Error parsing file parts for: {file_name}")
        return None
def data_valid_for_model(file_name, model_config, task_config):
    file_parts = parse_file_parts(file_name)
    if file_parts is None:
        print(f"Skipping invalid file format: {file_name}")
        return False  # Skip files with unrecognized format
    
    try:
        return (
            model_config.resolution in (0, float(file_parts.get("res", 0))) and
            len(task_config.pressure_levels) == int(file_parts.get("levels", 0)) and
            (
                ("total_precipitation_6hr" in task_config.input_variables and
                 file_parts.get("source") in ("era5", "fake")) or
                ("total_precipitation_6hr" not in task_config.input_variables and
                 file_parts.get("source") in ("hres", "fake"))
            )
        )
    except (TypeError, ValueError) as e:
        print(f"Error processing file '{file_name}': {e}")
        return False

# Filtering valid dataset options
# Create a dropdown widget for selecting the dataset file
dataset_file = widgets.Dropdown(
    options=[
        (", ".join([f"{k}: {v}" for k, v in parse_file_parts(option.removesuffix(".nc")).items()]), option)
        for option in dataset_file_options
        if data_valid_for_model(option, model_config, task_config)
    ],
    description="Dataset file:",
    layout={"width": "max-content"}
)
widgets.VBox([
    dataset_file,
    widgets.Label(value="Run the next cell to load the dataset. Rerunning this cell clears your selection and refilters the datasets that match your model.")
])

print(dataset_file)

# Check if the selected dataset file is valid
if not dataset_file.value or not data_valid_for_model(dataset_file.value, model_config, task_config):
    raise ValueError("Invalid dataset file, rerun the cell above and choose a valid dataset file.")

# Load dataset from the local file system
dataset_path = os.path.join(dataset_directory, dataset_file.value)
example_batch = xr.load_dataset(dataset_path).compute()

assert example_batch.dims["time"] >= 3  # 2 for input, >=1 for targets

# Display selected dataset metadata and content
print(", ".join([f"{k}: {v}" for k, v in parse_file_parts(dataset_file.value.removesuffix(".nc")).items()]))
print(example_batch)

plot_example_variable = widgets.Dropdown(
    options=example_batch.data_vars.keys(),
    value="2m_temperature",
    description="Variable")
plot_example_level = widgets.Dropdown(
    options=example_batch.coords["level"].values,
    value=500,
    description="Level")
plot_example_robust = widgets.Checkbox(value=True, description="Robust")
plot_example_max_steps = widgets.IntSlider(
    min=1, max=example_batch.dims["time"], value=example_batch.dims["time"],
    description="Max steps")

widgets.VBox([
    plot_example_variable,
    plot_example_level,
    plot_example_robust,
    plot_example_max_steps,
    widgets.Label(value="Run the next cell to plot the data. Rerunning this cell clears your selection.")
])


# @title Plot example data

plot_size = 7

data = {
    " ": scale(select(example_batch, plot_example_variable.value, plot_example_level.value, plot_example_max_steps.value),
              robust=plot_example_robust.value),
}
fig_title = plot_example_variable.value
if "level" in example_batch[plot_example_variable.value].coords:
  fig_title += f" at {plot_example_level.value} hPa"

plot_data(data, fig_title, plot_size, plot_example_robust.value)


# @title Choose training and eval data to extract
train_steps = widgets.IntSlider(
    value=1, min=1, max=example_batch.sizes["time"]-2, description="Train steps")
eval_steps = widgets.IntSlider(
    value=example_batch.sizes["time"]-2, min=1, max=example_batch.sizes["time"]-2, description="Eval steps")

widgets.VBox([
    train_steps,
    eval_steps,
    widgets.Label(value="Run the next cell to extract the data. Rerunning this cell clears your selection.")
])

# @title Extract training and eval data

train_inputs, train_targets, train_forcings = data_utils.extract_inputs_targets_forcings(
    example_batch, target_lead_times=slice("6h", f"{train_steps.value*6}h"),
    **dataclasses.asdict(task_config))

eval_inputs, eval_targets, eval_forcings = data_utils.extract_inputs_targets_forcings(
    example_batch, target_lead_times=slice("6h", f"{eval_steps.value*6}h"),
    **dataclasses.asdict(task_config))

print("All Examples:  ", example_batch.dims.mapping)
print("Train Inputs:  ", train_inputs.dims.mapping)
print("Train Targets: ", train_targets.dims.mapping)
print("Train Forcings:", train_forcings.dims.mapping)
print("Eval Inputs:   ", eval_inputs.dims.mapping)
print("Eval Targets:  ", eval_targets.dims.mapping)
print("Eval Forcings: ", eval_forcings.dims.mapping)


# # @title Load normalization data
stats_directory = "./stats"  # Replace with your actual path
# os.makedirs(stats_directory, exist_ok=True)

# # Initialize Google Cloud Storage client
# client = gcs_client
# bucket = gcs_bucket

# def download_file_from_gcs(gcs_file_path, local_file_path):
#     """Download a file from GCS to a local path."""
#     blob = bucket.blob(gcs_file_path)
#     blob.download_to_filename(local_file_path)
#     print(f"Downloaded {gcs_file_path} to {local_file_path}")

# # Define GCS file paths and local paths
files_to_download = {
    "stats/diffs_stddev_by_level.nc": os.path.join(stats_directory, "diffs_stddev_by_level.nc"),
    "stats/mean_by_level.nc": os.path.join(stats_directory, "mean_by_level.nc"),
    "stats/stddev_by_level.nc": os.path.join(stats_directory, "stddev_by_level.nc")
}

# # Download files if they do not already exist locally
# for gcs_file, local_file in files_to_download.items():
#     if not os.path.exists(local_file):
#         download_file_from_gcs(gcs_file, local_file)
#     else:
#         print(f"File already exists locally: {local_file}")

# Load the datasets with xarray
diffs_stddev_by_level = xr.load_dataset(files_to_download["stats/diffs_stddev_by_level.nc"]).compute()
mean_by_level = xr.load_dataset(files_to_download["stats/mean_by_level.nc"]).compute()
stddev_by_level = xr.load_dataset(files_to_download["stats/stddev_by_level.nc"]).compute()
# with gcs_bucket.blob("stats/diffs_stddev_by_level.nc").open("rb") as f:
#   diffs_stddev_by_level = xarray.load_dataset(f).compute()
# with gcs_bucket.blob("stats/mean_by_level.nc").open("rb") as f:
#   mean_by_level = xarray.load_dataset(f).compute()
# with gcs_bucket.blob("stats/stddev_by_level.nc").open("rb") as f:
#   stddev_by_level = xarray.load_dataset(f).compute()

  # @title Build jitted functions, and possibly initialize random weights
def construct_wrapped_graphcast(
    model_config: graphcast.ModelConfig,
    task_config: graphcast.TaskConfig):
  """Constructs and wraps the GraphCast Predictor."""
  # Deeper one-step predictor.
  predictor = graphcast.GraphCast(model_config, task_config)

  # Modify inputs/outputs to `graphcast.GraphCast` to handle conversion to
  # from/to float32 to/from BFloat16.
  predictor = casting.Bfloat16Cast(predictor)

  # Modify inputs/outputs to `casting.Bfloat16Cast` so the casting to/from
  # BFloat16 happens after applying normalization to the inputs/targets.
  predictor = normalization.InputsAndResiduals(
      predictor,
      diffs_stddev_by_level=diffs_stddev_by_level,
      mean_by_level=mean_by_level,
      stddev_by_level=stddev_by_level)

  # Wraps everything so the one-step model can produce trajectories.
  predictor = autoregressive.Predictor(predictor, gradient_checkpointing=True)
  return predictor


@hk.transform_with_state
def run_forward(model_config, task_config, inputs, targets_template, forcings):
  predictor = construct_wrapped_graphcast(model_config, task_config)
  return predictor(inputs, targets_template=targets_template, forcings=forcings)


@hk.transform_with_state
def loss_fn(model_config, task_config, inputs, targets, forcings):
  predictor = construct_wrapped_graphcast(model_config, task_config)
  loss, diagnostics = predictor.loss(inputs, targets, forcings)
  return xarray_tree.map_structure(
      lambda x: xarray_jax.unwrap_data(x.mean(), require_jax=True),
      (loss, diagnostics))

def grads_fn(params, state, model_config, task_config, inputs, targets, forcings):
  def _aux(params, state, i, t, f):
    (loss, diagnostics), next_state = loss_fn.apply(
        params, state, jax.random.PRNGKey(0), model_config, task_config,
        i, t, f)
    return loss, (diagnostics, next_state)
  (loss, (diagnostics, next_state)), grads = jax.value_and_grad(
      _aux, has_aux=True)(params, state, inputs, targets, forcings)
  return loss, diagnostics, next_state, grads

# Jax doesn't seem to like passing configs as args through the jit. Passing it
# in via partial (instead of capture by closure) forces jax to invalidate the
# jit cache if you change configs.
def with_configs(fn):
  return functools.partial(
      fn, model_config=model_config, task_config=task_config)

# Always pass params and state, so the usage below are simpler
def with_params(fn):
  return functools.partial(fn, params=params, state=state)

# Our models aren't stateful, so the state is always empty, so just return the
# predictions. This is requiredy by our rollout code, and generally simpler.
def drop_state(fn):
  return lambda **kw: fn(**kw)[0]

init_jitted = jax.jit(with_configs(run_forward.init))

if params is None:
  params, state = init_jitted(
      rng=jax.random.PRNGKey(0),
      inputs=train_inputs,
      targets_template=train_targets,
      forcings=train_forcings)

loss_fn_jitted = drop_state(with_params(jax.jit(with_configs(loss_fn.apply))))
grads_fn_jitted = with_params(jax.jit(with_configs(grads_fn)))
run_forward_jitted = drop_state(with_params(jax.jit(with_configs(
    run_forward.apply))))



# @title Autoregressive rollout (loop in python)

assert model_config.resolution in (0, 360. / eval_inputs.sizes["lon"]), (
  "Model resolution doesn't match the data resolution. You likely want to "
  "re-filter the dataset list, and download the correct data.")

print("Inputs:  ", eval_inputs.dims.mapping)
print("Targets: ", eval_targets.dims.mapping)
print("Forcings:", eval_forcings.dims.mapping)

predictions = rollout.chunked_prediction(
    run_forward_jitted,
    rng=jax.random.PRNGKey(0),
    inputs=eval_inputs,
    targets_template=eval_targets * np.nan,
    forcings=eval_forcings)
print(predictions)
predictions.to_netcdf("predictions.nc")

# @title Choose predictions to plot

plot_pred_variable = widgets.Dropdown(
    options=predictions.data_vars.keys(),
    value="2m_temperature",
    description="Variable")
plot_pred_level = widgets.Dropdown(
    options=predictions.coords["level"].values,
    value=500,
    description="Level")
plot_pred_robust = widgets.Checkbox(value=True, description="Robust")
plot_pred_max_steps = widgets.IntSlider(
    min=1,
    max=predictions.dims["time"],
    value=predictions.dims["time"],
    description="Max steps")

widgets.VBox([
    plot_pred_variable,
    plot_pred_level,
    plot_pred_robust,
    plot_pred_max_steps,
    widgets.Label(value="Run the next cell to plot the predictions. Rerunning this cell clears your selection.")
])


# @title Plot predictions

plot_size = 5
plot_max_steps = min(predictions.dims["time"], plot_pred_max_steps.value)

data = {
    "Targets": scale(select(eval_targets, plot_pred_variable.value, plot_pred_level.value, plot_max_steps), robust=plot_pred_robust.value),
    "Predictions": scale(select(predictions, plot_pred_variable.value, plot_pred_level.value, plot_max_steps), robust=plot_pred_robust.value),
    "Diff": scale((select(eval_targets, plot_pred_variable.value, plot_pred_level.value, plot_max_steps) -
                        select(predictions, plot_pred_variable.value, plot_pred_level.value, plot_max_steps)),
                       robust=plot_pred_robust.value, center=0),
}
fig_title = plot_pred_variable.value
if "level" in predictions[plot_pred_variable.value].coords:
  fig_title += f" at {plot_pred_level.value} hPa"

plot_data(data, fig_title, plot_size, plot_pred_robust.value)
