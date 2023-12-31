import math
import pandas_datareader as web
import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import yfinance as yf
import plotly.graph_objs as go
import plotly.express as px
import requests

def update_chart(selected_stock, start_date, end_date, button_press, future_button):
    if selected_stock is not None:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        print(start_date)
        yf.pdr_override()

        # Load stock data
        df = yf.download(tickers=selected_stock, start=start_date, end=end_date)

        # Create a plot for the closing price history
        trace = go.Scatter(x=df.index, y=df["Close"], mode="lines", name="Close Price")
        layout = go.Layout(
            title="Close Price History",
            xaxis=dict(title="Date"),
            yaxis=dict(title="Close Price USD ($)")
        )
        fig = go.Figure(data=[trace], layout=layout)
        
        if button_press == 1:
            # Create a new DataFrame with only the "Close" column
            data = df.filter(["Close"])

            # Convert the DataFrame to a Numpy array
            dataset = data.values

            # Scale the data
            scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_data = scaler.fit_transform(dataset)

            # Split the data into training and temporary data
            training_data_len = math.ceil(len(dataset) * 0.8)
            train_data = scaled_data[0:training_data_len, :]

            x_train = []
            y_train = []

            for i in range(60, len(train_data)):
                x_train.append(train_data[i-60:i, 0])
                y_train.append(train_data[i, 0])

            x_train, y_train = np.array(x_train), np.array(y_train)
            x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

            # Build the LSTM model
            model = Sequential()
            model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
            model.add(LSTM(50, return_sequences=False))
            model.add(Dense(25))
            model.add(Dense(1))

            # Compile the model
            model.compile(optimizer="adam", loss="mean_squared_error")

            # Train the model
            model.fit(x_train, y_train, batch_size=16, epochs=5)

            # Create temporary data set
            temp_data = scaled_data[training_data_len - 60:, :]
            x_temp = []
            y_temp = dataset[training_data_len:, :]

            for i in range(60, len(temp_data)):
                x_temp.append(temp_data[i-60:i, 0])

            x_temp = np.array(x_temp)
            x_temp = np.reshape(x_temp, (x_temp.shape[0], x_temp.shape[1], 1))

            predictions = model.predict(x_temp)
            predictions = scaler.inverse_transform(predictions)

            rmse = np.sqrt(np.mean(predictions - y_temp) ** 2)
            print(rmse)

            train = data[:training_data_len]
            valid = data[training_data_len:]
            valid["Predictions"] = predictions

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=train.index, y=train["Close"], mode="lines", name="Train"))
            fig.add_trace(go.Scatter(x=valid.index, y=valid["Close"], mode="lines", name="Validation"))
            fig.add_trace(go.Scatter(x=valid.index, y=valid["Predictions"], mode="lines", name="Predictions"))
            fig.update_layout(title="Model", xaxis_title="Date", yaxis_title="Close Price USD ($)")
            
            if future_button == 1:
                temp = []
                temp.append(scaled_data[-60:])
                temp = np.array(temp)
                temp = np.reshape(temp, (temp.shape[0], temp.shape[1], 1))
                real_predictions = []
                x_achse = []

                for i in range(30):
                    x_achse.append(i)
                    predictions_temp = model.predict(temp)
                    predictions_temp = np.reshape(predictions_temp, (1, 1, 1))

                    temp = temp[:, 1:, :]
                    temp = np.concatenate((temp, predictions_temp), axis=1)

                    temp = np.array(temp)
                    temp = np.reshape(temp, (temp.shape[0], temp.shape[1], 1))

                    predictions_temp = scaler.inverse_transform(np.reshape(predictions_temp, (1, 1)))

                    real_predictions.append(predictions_temp[0][0])

                trace_pred = go.Scatter(x=x_achse, y=real_predictions, mode="lines", name="Predictions for the next 30 Days")
                layout = go.Layout(
                    title="Predictions for the next 30 Days",
                    xaxis=dict(title="Days"),
                    yaxis=dict(title="Close Price USD ($)")
                )
                fig = go.Figure(data=[trace_pred], layout=layout)
                
        return fig, ""
    else:
        return {}, ""
