import dash
from dash import dcc, html
import pandas as pd
from data import nasdaq_dict  # Make sure to import data from a valid source

def get_layout():
    # Create dropdown options from nasdaq_dict
    dropdown_options = [{"label": company_name, "value": symbol} for symbol, company_name in nasdaq_dict.items()]

    return html.Div([
        # Content for Stock Prediction
        html.H2("Stock Prediction"),
        html.P(
            "On this page, you can select a stock and train a neural network to make predictions for the next few days. "
            "To do this, select a stock and the observation period. Then, press the 'Train' button (this may take some time "
            "as the server's computing power is limited). Click 'Predict the next 30 days' to see predictions on a graph."
        ),
        dcc.DatePickerSingle(
            id="start-date-picker",
            date=pd.to_datetime("2015-03-15"),
            display_format="YYYY-MM-DD",
        ),
        dcc.DatePickerSingle(
            id="end-date-picker",
            date=pd.to_datetime("2020-03-15"),
            display_format="YYYY-MM-DD",
        ),
        html.Button("Train", id="train-button"),
        html.Button("Predict the next 30 days", id="future-button"),
        dcc.Dropdown(
            id="nasdaq-dropdown",
            options=dropdown_options,
            multi=False,
            placeholder="Select a stock name"
        ),
        dcc.Graph(id="stock-price-graph"),

        html.Div([
            html.P(
                "Research Question: How good is a neural network trained on past prices at predicting future stock prices?",
                style={"fontSize": 30}
            ),
            html.P(
                "For the AAPL example below, the network was trained on 5 years of data and is reasonably good at predicting "
                "stock prices. If you use less data, its performance may decline. However, remember that it may not be accurate "
                "enough for investment decisions."
            )
        ]),
        html.Div(id="selected-stock-text"),
        html.Img(src="assets/apple_stock_prediction.png", style={"max-width": "100%"}),
        html.Img(src="assets/apple30dayspred.png", style={"max-width": "100%"}),
    ])
