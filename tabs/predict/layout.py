import dash
from dash import dcc, html
import pandas as pd
from data import nasdaq_dict

def get_layout():
    dropdown_options = [{'label': company_name, 'value': symbol} for symbol, company_name in nasdaq_dict.items()]
    return html.Div([
        # Content for Event Analysis
        html.H2("Stock Prediction"),
        html.P("On this page it is possible to select a stock and then train a neural network to make predictions for the next few days. All you have to do is select a share and the observation period. Afterwards, the network is trained by pressing the train button (this can take some time, as the computing power of the server is very weak). By clicking on predictions for the next days, you will receive a graph with the predictions for the next days."),
        dcc.DatePickerSingle(
        id='start-date-picker',
        date=pd.to_datetime('2015-03-15'),
        display_format='YYYY-MM-DD',
        ),
        dcc.DatePickerSingle(
        id='end-date-picker',
        date=pd.to_datetime('2020-03-15'),
        display_format='YYYY-MM-DD',
        ),
        html.Button("Train", id="train-button"),
        html.Button("Predict the next 30 days", id="future-button"),
        # dcc.Input(id= 'stock-search', type = "text", placeholder = "Search Stocks"),

        dcc.Dropdown(
            id='nasdaq-dropdown',
            options=dropdown_options,
            multi=False,
            placeholder="Select a stock name"
        ),
        # dcc.Dropdown(
        #     id='stock-dropdown',
        #     options=[],
        #     multi=False,
        #     placeholder="Select a stock name"
        # ),
        dcc.Graph(id='stock-price-graph'),

                html.Div([
                    html.P("Research Question: How good is a neural network trained on past prices at predicting the future stock prices", style={'fontSize': 30}),
                    html.P("For the AAPL example below the network was trained on 5 years of data and is pretty good at predicting the stock price. If you give it less data it performs worse, but either way it is not accurate enough to warrant basing your investments on it")

                ]),
        html.Div(id='selected-stock-text'),
        html.Img(src='assets/apple_stock_prediction.png', style={'max-width':'100%'}),
        html.Img(src='assets/apple30dayspred.png', style={'max-width':'100%'}),

       
    ])