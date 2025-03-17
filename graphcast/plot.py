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

predictions_path = "predictions.nc"  # Đường dẫn đến tệp của bạn
predictions = xr.load_dataset(predictions_path)

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
# Hàm plot_data sửa để hiển thị ngay trong Python
def plot_data(
    data: dict[str, tuple[xr.Dataset, matplotlib.colors.Normalize, str]],
    fig_title: str,
    plot_size: float = 5,
    robust: bool = False,
    cols: int = 4
    ):
    
    first_data = next(iter(data.values()))[0]
    max_steps = first_data.sizes.get("time", 1)
    
    cols = min(cols, len(data))
    rows = math.ceil(len(data) / cols)
    figure = plt.figure(figsize=(plot_size * 2 * cols, plot_size * rows))
    figure.suptitle(fig_title, fontsize=16)
    figure.subplots_adjust(wspace=0, hspace=0)
    
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

    ani = animation.FuncAnimation(figure, update, frames=max_steps, interval=250)
    plt.show()

# Gán trực tiếp các giá trị thay cho widgets
plot_pred_variable_value = "total_precipitation_6hr"  # Biến muốn hiển thị
plot_pred_level_value = 500  # Mức áp suất cần hiển thị
plot_pred_robust_value = True  # Sử dụng robust scale
plot_pred_max_steps_value = predictions.dims["time"]  # Số bước thời gian tối đa

# Thiết lập và chuyển đổi dữ liệu cho hàm plot_data
plot_size = 5
plot_max_steps = min(predictions.dims["time"], plot_pred_max_steps_value)

data = {
   # "Targets": scale(select(eval_targets, plot_pred_variable_value, plot_pred_level_value, plot_max_steps), robust=plot_pred_robust_value),
    "Predictions": scale(select(predictions, plot_pred_variable_value, plot_pred_level_value, plot_max_steps), robust=plot_pred_robust_value),
    # "Diff": scale(
    #     (select(eval_targets, plot_pred_variable_value, plot_pred_level_value, plot_max_steps) - 
    #      select(predictions, plot_pred_variable_value, plot_pred_level_value, plot_max_steps)),
    #     robust=plot_pred_robust_value, center=0
    # ),
}

# Tạo tiêu đề cho biểu đồ
fig_title = plot_pred_variable_value
if "level" in predictions[plot_pred_variable_value].coords:
    fig_title += f" at {plot_pred_level_value} hPa"

# Gọi hàm plot_data để hiển thị biểu đồ
plot_data(data, fig_title, plot_size, plot_pred_robust_value)