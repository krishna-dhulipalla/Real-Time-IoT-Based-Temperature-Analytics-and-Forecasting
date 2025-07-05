import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Conv1D, Flatten
from sklearn.model_selection import train_test_split
from statsmodels.tsa.arima.model import ARIMA


def generate_series(length=2000):
    rng = pd.date_range('2024-01-01', periods=length, freq='H')
    data = np.sin(np.linspace(0, 50, length)) + np.random.normal(scale=0.5, size=length)
    return pd.Series(data, index=rng, name='temperature')


def train_lstm(series):
    X = []
    y = []
    values = series.values
    for i in range(len(values) - 10):
        X.append(values[i:i+10])
        y.append(values[i+10])
    X = np.array(X)[..., np.newaxis]
    y = np.array(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = Sequential([
        LSTM(32, input_shape=(10,1)),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    model.fit(X_train, y_train, epochs=5, verbose=0)
    return model.evaluate(X_test, y_test, verbose=0)


def train_cnn(series):
    X = []
    y = []
    values = series.values
    for i in range(len(values) - 10):
        X.append(values[i:i+10])
        y.append(values[i+10])
    X = np.array(X)[..., np.newaxis]
    y = np.array(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = Sequential([
        Conv1D(32, 3, activation='relu', input_shape=(10,1)),
        Flatten(),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    model.fit(X_train, y_train, epochs=5, verbose=0)
    return model.evaluate(X_test, y_test, verbose=0)


def train_arima(series):
    model = ARIMA(series, order=(2,0,2)).fit()
    forecast = model.forecast(steps=10)
    return forecast.iloc[-1]


if __name__ == '__main__':
    s = generate_series()
    lstm_loss = train_lstm(s)
    cnn_loss = train_cnn(s)
    arima_pred = train_arima(s)
    print(f"LSTM loss: {lstm_loss}")
    print(f"CNN loss: {cnn_loss}")
    print(f"ARIMA last forecast: {arima_pred}")
