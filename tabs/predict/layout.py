import dash
from dash import dcc, html
import pandas as pd
from data import nasdaq_dict

def get_layout():
    dropdown_options = [{'label': company_name, 'value': symbol} for symbol, company_name in nasdaq_dict.items()]
    return html.Div([
        # Content for Event Analysis
        html.H2("Stock Prediction"),
        html.P(""),
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

        
        html.Div(id='selected-stock-text', style={'fontSize': 22}),

       
    ])