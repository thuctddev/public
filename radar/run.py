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

dataset = create_dataset_from_raw('./raw/raw_training/', resize_to=(315,344))
dataset = np.expand_dims(dataset, axis=-1)
dataset_x, dataset_y = create_shifted_frames(dataset)
X_train, X_val, y_train, y_val = sk.train_test_split(dataset_x,dataset_y,test_size=0.2, random_state = 42)


def create_model():
    model = Sequential()
    model.add(ConvLSTM2D(filters=64, kernel_size=(7, 7),
                    input_shape=(18,344,315,1),
                    padding='same',activation=LeakyReLU(alpha=0.01), 
                    return_sequences=True))
    model.add(BatchNormalization())
    model.add(ConvLSTM2D(filters=64, kernel_size=(5, 5),
                    padding='same',activation=LeakyReLU(alpha=0.01), 
                    return_sequences=True))
    model.add(BatchNormalization())
    model.add(ConvLSTM2D(filters=64, kernel_size=(3, 3),
                    padding='same',activation=LeakyReLU(alpha=0.01), 
                    return_sequences=True))
    model.add(BatchNormalization())
    model.add(ConvLSTM2D(filters=64, kernel_size=(1, 1),
                    padding='same',activation=LeakyReLU(alpha=0.01), 
                    return_sequences=True))
    model.add(BatchNormalization())
    model.add(Conv3D(filters=1, kernel_size=(3,3,3),
                activation='sigmoid',
                padding='same', data_format='channels_last'))
    return model

model = create_model()

model.compile(loss='binary_crossentropy', optimizer='adadelta')
print(model.summary())
# Define modifiable training hyperparameters.
epochs = 25
batch_size = 1

#Fit the model to the training data.
model.fit(
    X_train,
    y_train,
    batch_size=batch_size,
    epochs=epochs,
    validation_data=(X_val, y_val),
    verbose=1,
)
# # model.save('./model_saved')
model.save('./model_saved.h5')

from tensorflow.keras.models import load_model
from tensorflow.keras.layers import LeakyReLU
model = load_model('./model_saved.h5', custom_objects={'LeakyReLU': LeakyReLU})

# reconstructed_model = keras.models.load_model("./drive/MyDrive/model_saved")
# pick a random index from validation dataset
random_index = np.random.choice(range(len(X_val)), size=1)
test_serie_X = X_val[random_index[0]]
test_serie_Y = y_val[random_index[0]]

first_frames = test_serie_X
original_frames = test_serie_Y
# predict the next 18 fames
new_prediction = model.predict(np.expand_dims(first_frames, axis=0))
new_prediction = np.squeeze(new_prediction, axis=0)

fig, axes = plt.subplots(2, 18, figsize=(20, 4))

# Plot the original frames.
for idx, ax in enumerate(axes[0]):
    ax.imshow(np.squeeze(original_frames[idx]), cmap="viridis")
    ax.set_title(f"Frame {idx + 18}")
    ax.axis("off")

# Plot the predicted frames.
for idx, ax in enumerate(axes[1]):
    ax.imshow((new_prediction[idx]).reshape((344,315)), cmap="viridis")
    ax.set_title(f"Frame {idx + 18}")
    ax.axis("off")

# Display the figure.
plt.show()

fig, ax = plt.subplots()
original_images = []
for f in original_frames:
    ax.set_title(f"Ground Truth")
    ax.axis("off")
    crn_f = ax.imshow(np.squeeze(f),cmap='viridis', animated=False)
    original_images.append([crn_f])
animation_originals = animation.ArtistAnimation(fig, original_images, 
                                                interval=100, blit=False, 
                                                repeat_delay=1000)
animation_originals.save('./ground_truth.gif', 
                         writer=animation.PillowWriter(), dpi=100)


fig, ax = plt.subplots()
predicted_images = []
for f in new_prediction:
    ax.set_title(f"Ground Truth")
    ax.axis("off")
    crn_f = ax.imshow(np.squeeze(f),cmap='viridis', animated=False)
    ax.set_title(f"Predicted frames")
    predicted_images.append([crn_f])
print(len(predicted_images))
animation_predicted = animation.ArtistAnimation(fig, predicted_images, 
                                                interval=100, blit=False, 
                                                repeat_delay=1000)
animation_predicted.save('./predicted.gif', 
                         writer=animation.PillowWriter(), dpi=100)
