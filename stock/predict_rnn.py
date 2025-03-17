import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
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

# Tạo tập kiểm tra
X_test, y_test = create_dataset(test_data, time_step, target_col=target_column_index, forecast_days=forecast_days)

# Chuyển đổi dữ liệu đầu vào thành định dạng [samples, time steps, features]
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], X_test.shape[2])

# Danh sách các phương pháp để tải mô hình và dự báo
methods = ['LSTM', 'RNN', 'GRU', 'CNN', 'MLP', 'CNN-LSTM']
predictions_test = []
ensemble_predictions = []

# Chuyển đổi giá trị thực tế của tập kiểm tra về không gian gốc
y_test_rescaled = scaler_target.inverse_transform(y_test.reshape(-1, 1))

for method in methods:
    print(f'Đang tải và dự báo với mô hình {method}')
    
    # Load mô hình đã huấn luyện
    model = load_model(f'model/model_{method}.h5')
    
    # Dự báo trên tập kiểm tra
    if method == 'MLP':
        X_test_flatten = X_test.reshape(X_test.shape[0], -1)
        y_test_pred = model.predict(X_test_flatten)
    else:
        y_test_pred = model.predict(X_test)
    
    # Chuyển đổi dự báo về không gian gốc
    y_test_pred_rescaled = scaler_target.inverse_transform(y_test_pred)
    ensemble_predictions.append(y_test_pred_rescaled)
    
    # Tính RMSE
    rmse = math.sqrt(mean_squared_error(y_test_rescaled, y_test_pred_rescaled))
    predictions_test.append((method, y_test_pred_rescaled, rmse))

# Tính toán dự báo ensemble (trung bình của các phương pháp)
ensemble_mean = np.mean(ensemble_predictions, axis=0)
ensemble_std = np.std(ensemble_predictions, axis=0)
ensemble_rmse = math.sqrt(mean_squared_error(y_test_rescaled, ensemble_mean))

# Vẽ tất cả các đường dự báo trong cùng một biểu đồ
plt.figure(figsize=(14, 7))
plt.plot(test_dates, y_test_rescaled, label='Thực tế', linewidth=2, color='black')

# Vẽ các đường dự báo từ các phương pháp khác nhau và hiển thị RMSE trong legend
for method, prediction, rmse in predictions_test:
    plt.plot(test_dates, prediction, label=f'Dự đoán - {method} (RMSE: {rmse:.2f})')

# Vẽ đường dự báo ensemble và vùng tán (độ lệch chuẩn)
#plt.plot(test_dates, ensemble_mean, label=f'Ensemble (RMSE: {ensemble_rmse:.2f})', linewidth=2, linestyle='--', color='blue')
#plt.fill_between(test_dates, (ensemble_mean - ensemble_std).flatten(), (ensemble_mean + ensemble_std).flatten(), color='blue', alpha=0.2, label='Ensemble trend')

plt.legend()
plt.title('So sánh các phương pháp dự báo giá đóng cửa 3 ngày tới')
plt.xlabel('Thời gian')
plt.ylabel('Giá trị')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
