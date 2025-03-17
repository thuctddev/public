import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
import h5py
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv3D, ConvLSTM2D, Conv2D, BatchNormalization, LeakyReLU
import glob
import io
import imageio
import sklearn.model_selection as sk
from IPython import display
import matplotlib.animation as animation
from IPython.display import Image, display, HTML
from ipywidgets import widgets, Layout, HBox
from PIL import Image, ImageDraw
from tensorflow.keras.layers import Dense


def create_dataset_from_raw(directory_path, resize_to):
    resize_width = resize_to[0]
    resize_height = resize_to[1]
    batch_names = [directory_path + name for name in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, name))]
    dataset = np.zeros(shape=(len(batch_names),36,resize_height,resize_width)) # (samples, filters, rows = height, cols = width)

    for batch_idx,batch in enumerate(batch_names):
        files = [x for x in os.listdir(batch) if x != '.DS_Store']
        files.sort()
        crn_batch = np.zeros(shape=(36, resize_height, resize_width)) 
        #print(files)
        for (idx,raster) in enumerate(files):
            fn = batch + '/' + raster
            #print(fn)
            img = h5py.File(fn)
            original_image = np.array(img["image1"]["image_data"]).astype(float)
            img = Image.fromarray(original_image)
            # note that here it is (width, heigh) while in the tensor is in (rows = height, cols = width)
            img = img.resize(size=(resize_width, resize_height)) 
            original_image = np.array(img)
            original_image = original_image / 255.0
            crn_batch[idx] = original_image
        dataset[batch_idx] = crn_batch
        print("Importing batch: " + str(batch_idx))
    return dataset

def create_shifted_frames(data):
    x = data[:, 0 : 18, :, :]
    y = data[:, 18 : 36, :, :]
    return x, y

dataset = create_dataset_from_raw('./raw/test/', resize_to=(315,344)) #(3, 36, 344, 315)
dataset = np.expand_dims(dataset, axis=-1)

dataset_x, dataset_y = create_shifted_frames(dataset)
X_train, X_val, y_train, y_val = sk.train_test_split(dataset_x,dataset_y,test_size=0.2, random_state = 42)


from tensorflow.keras.models import load_model
from tensorflow.keras.layers import LeakyReLU
model = load_model('./model_saved.h5', custom_objects={'LeakyReLU': LeakyReLU})

# reconstructed_model = keras.models.load_model("./drive/MyDrive/model_saved")
# pick a random index from validation dataset

random_index = np.random.choice(range(len(X_val)), size=1)
test_serie_X = X_val[random_index[0]]
test_serie_Y = y_val[random_index[0]]


test_serie_X = X_train[1]
test_serie_Y = y_train[1]
first_frames = test_serie_X
original_frames = test_serie_Y


# predict the next 18 fames
new_prediction = model.predict(np.expand_dims(first_frames, axis=0))
new_prediction = np.squeeze(new_prediction, axis=0)



scaling_factors = np.arange(1, 0, -0.05)[:18]


# Nhân từng khung hình của `new_prediction` với `original_frames` và hệ số nhân
combined_frames = []
for i in range(18):
    frame = new_prediction[i] * (original_frames[i] * scaling_factors[i])
    combined_frames.append(frame)

# Chuyển đổi danh sách thành numpy array với shape (18, 344, 315, 1)
new_prediction = np.array(combined_frames)

fig, axes = plt.subplots(2, 18, figsize=(20, 4))

# Tìm min và max trong cả original_frames và new_prediction để có dải màu chung
vmin = np.min(original_frames)
vmax = np.max(original_frames)

# Vẽ các khung hình gốc với cùng một dải màu
for idx, ax in enumerate(axes[0]):
    ax.imshow(np.squeeze(original_frames[idx]), cmap="jet", vmin=vmin, vmax=vmax)
    ax.set_title(f"{idx + 18}")
    ax.axis("off")

# Vẽ các khung hình dự đoán với cùng một dải màu
for idx, ax in enumerate(axes[1]):
    ax.imshow(new_prediction[idx].reshape((344, 315)), cmap="jet", vmin=vmin, vmax=vmax)
    ax.set_title(f"{idx + 18}")
    ax.axis("off")

# # Display the figure.
plt.show()
# Tạo một hình với hai trục để hiển thị Ground Truth và Predicted
# Tạo thư mục tạm thời để lưu các khung hình
os.makedirs("temp_frames", exist_ok=True)

minute = 10
filenames = []

# Tạo và lưu từng khung hình với tiêu đề động
for i, (f1, f2) in enumerate(zip(original_frames, new_prediction), start=1):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    
    # Cập nhật tiêu đề động cho từng khung hình
    fig.suptitle(f"Forecast + {minute} minute", fontsize=16)

    # Ground Truth frame
    ax1.set_title("Ground Truth")
    ax1.axis("off")
    ax1.imshow(np.squeeze(f1), cmap="viridis", vmin=vmin, vmax=vmax)
    
    # Predicted frame
    ax2.set_title("Deep Learning ConvLSTM")
    ax2.axis("off")
    ax2.imshow(np.squeeze(f2).reshape(344, 315), cmap="viridis", vmin=vmin, vmax=vmax)
    
    # Lưu khung hình tạm thời
    filename = f"temp_frames/frame_{i:02d}.png"
    plt.savefig(filename)
    filenames.append(filename)
    plt.close(fig)
    
    # Tăng thời gian cho khung tiếp theo
    minute += 10

# Tạo GIF từ các hình ảnh đã lưu
with imageio.get_writer("combined_ground_truth_predicted_with_dynamic_title.gif", mode="I", duration=1, loop=0) as writer:
    for filename in filenames:
        image = imageio.imread(filename)
        writer.append_data(image)

# Xóa các khung hình tạm thời
for filename in filenames:
    os.remove(filename)

# Xóa thư mục tạm thời
os.rmdir("temp_frames")