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
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import LeakyReLU
# Thiết lập Matplotlib để lưu ảnh mà không cần giao diện tương tác
matplotlib.use("Agg")

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

dataset = create_dataset_from_raw('./raw/raw_validation/', resize_to=(315,344))
dataset = np.expand_dims(dataset, axis=-1)
dataset_x, dataset_y = create_shifted_frames(dataset)
X_train, X_val, y_train, y_val = sk.train_test_split(dataset_x,dataset_y,test_size=0.2, random_state = 42)


# Tải mô hình đã lưu và chỉ định các lớp tùy chỉnh nếu có
model = load_model('./model_saved.h5', custom_objects={'LeakyReLU': LeakyReLU})

# Kiểm tra cấu trúc mô hình
print(model.summary())

# Xác định lại các tham số huấn luyện
epochs = 2  # Số epochs để tiếp tục huấn luyện
batch_size = 1  # Kích thước batch

# Biên dịch mô hình lại (nếu cần) với loss và optimizer tương tự
model.compile(loss='binary_crossentropy', optimizer='adadelta')

# Tiếp tục huấn luyện mô hình với dữ liệu đã chuẩn bị
model.fit(
    X_train,
    y_train,
    batch_size=batch_size,
    epochs=epochs,
    validation_data=(X_val, y_val),
    verbose=1,
)

# Lưu lại mô hình sau khi huấn luyện thêm
model.save('./model_saved_updated.h5')
