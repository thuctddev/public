import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, GRU, SimpleRNN, Conv1D, Flatten, Dropout
from tensorflow.keras.layers import MaxPooling1D
import math
from sklearn.metrics import mean_squared_error

# Đọc dữ liệu từ file HDG.dat bằng pandas và bỏ qua hàng đầu tiên
file_path = 'HDG.dat'
df = pd.read_csv(file_path, sep='\s+', header=None, skiprows=1)

# Chuyển cột đầu tiên thành thời gian
df[0] = pd.to_datetime(df[0], format='%Y-%m-%d')

# Lưu các giá trị thời gian để sử dụng trong plot
dates = df[0].values

# Loại bỏ cột thời gian và chỉ lấy 55 cột đầu tiên
valid_data = df.dropna().iloc[:, 1:55].values

# Chuẩn hóa dữ liệu cho toàn bộ cột
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_features = scaler.fit_transform(valid_data)

# Lấy cột thứ 4 (cột 3 theo chỉ mục 0-based) làm cột dự báo
target_column_index = 3
# Tạo scaler riêng cho cột thứ 4 để sử dụng khi "inverse scaling"
scaler_target = MinMaxScaler(feature_range=(0, 1))
scaler_target.fit(valid_data[:, target_column_index].reshape(-1, 1))

# Định nghĩa các biến time_step và forecast_days trước khi cắt mảng dates
time_step = 100
forecast_days = 3

# Chia dữ liệu thành tập huấn luyện và kiểm tra
training_size = int(len(scaled_features) * 0.8)
test_size = len(scaled_features) - training_size
train_data, test_data = scaled_features[0:training_size, :], scaled_features[training_size:len(scaled_features), :]

# Cắt mảng dates tương ứng với tập kiểm tra
test_dates = dates[training_size + time_step + forecast_days - 1:]

# Hàm tạo tập dữ liệu dự báo cho ngày thứ 3
def create_dataset(dataset, time_step=1, target_col=3, forecast_days=3):
    dataX, dataY = [], []
    for i in range(len(dataset) - time_step - forecast_days + 1):
        dataX.append(dataset[i:(i + time_step)])
        dataY.append(dataset[i + time_step + forecast_days - 1, target_col])  # Lấy giá trị sau 'forecast_days' ngày làm đầu ra
    return np.array(dataX), np.array(dataY)

# Tạo tập huấn luyện và kiểm tra
X_train, y_train = create_dataset(train_data, time_step, target_col=target_column_index, forecast_days=forecast_days)
X_test, y_test = create_dataset(test_data, time_step, target_col=target_column_index, forecast_days=forecast_days)

# Chuyển đổi dữ liệu đầu vào thành định dạng [samples, time steps, features]
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], X_train.shape[2])
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], X_test.shape[2])

# Hàm tạo mô hình LSTM, RNN, GRU, CNN, MLP, và CNN-LSTM
def create_model(model_type, input_shape):
    model = Sequential()
    if model_type == 'LSTM':
        model.add(LSTM(100, return_sequences=True, input_shape=input_shape, activation='relu'))
        model.add(LSTM(100, activation='relu'))
    elif model_type == 'RNN':
        model.add(SimpleRNN(100, return_sequences=True, input_shape=input_shape, activation='relu'))
        model.add(SimpleRNN(100, activation='relu'))
    elif model_type == 'GRU':
        model.add(GRU(100, return_sequences=True, input_shape=input_shape, activation='relu'))
        model.add(GRU(100, activation='relu'))
    elif model_type == 'CNN':
        model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=input_shape))
        model.add(MaxPooling1D(pool_size=2))
        model.add(Flatten())
    elif model_type == 'MLP':
        model.add(Dense(128, activation='relu', input_shape=(input_shape[0] * input_shape[1],)))
        model.add(Dense(64, activation='relu'))
    elif model_type == 'CNN-LSTM':
        model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=input_shape))
        model.add(MaxPooling1D(pool_size=2))
        model.add(LSTM(100, activation='relu'))
    
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model

# Danh sách các phương pháp để thử nghiệm
methods = ['LSTM', 'RNN', 'GRU', 'CNN', 'MLP', 'CNN-LSTM']
predictions_test = []

# Chuyển đổi giá trị thực tế của tập kiểm tra về không gian gốc
y_test_rescaled = scaler_target.inverse_transform(y_test.reshape(-1, 1))

for method in methods:
    print(f'Đang huấn luyện mô hình {method}')
    
    if method == 'MLP':
        X_train_flatten = X_train.reshape(X_train.shape[0], -1)
        X_test_flatten = X_test.reshape(X_test.shape[0], -1)
        model = create_model(method, (X_train.shape[1], X_train.shape[2]))
        model.fit(X_train_flatten, y_train, validation_data=(X_test_flatten, y_test), epochs=100, batch_size=10, verbose=1)
        y_test_pred = model.predict(X_test_flatten)
    else:
        model = create_model(method, (time_step, X_train.shape[2]))
        model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=100, batch_size=10, verbose=1)
        y_test_pred = model.predict(X_test)
    
    model.save(f'model/model_{method}.h5')
    
    # Chỉ áp dụng inverse scaling lên cột dự báo
    y_test_pred_rescaled = scaler_target.inverse_transform(y_test_pred)
    
    # Tính RMSE
    rmse = math.sqrt(mean_squared_error(y_test_rescaled, y_test_pred_rescaled))
    predictions_test.append((method, y_test_pred_rescaled, rmse))

# Vẽ tất cả các đường dự báo trong cùng một biểu đồ
plt.figure(figsize=(14, 7))
plt.plot(test_dates, y_test_rescaled, label='Thực tế', linewidth=2, color='black')

# Vẽ các đường dự báo từ các phương pháp khác nhau và hiển thị RMSE trong legend
for method, prediction, rmse in predictions_test:
    plt.plot(test_dates, prediction, label=f'Dự đoán - {method} (RMSE: {rmse:.2f})')

plt.legend()
plt.title('So sánh các phương pháp dự báo giá đóng cửa 10 ngày tới')
plt.xlabel('Thời gian')
plt.ylabel('Giá trị')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
