import dash
from dash import dcc, html
import pandas as pd
from data import sector_stock_data_dict as stock_data_dict

def get_layout():
    return html.Div([
        # Content for Event Analysis
        html.H2("Sector Performance Analysis"),
        html.P(""),
        dcc.DatePickerSingle(
        id='event-date-picker',
        date=pd.to_datetime('2020-03-15'),
        display_format='YYYY-MM-DD',
        style = {'display': 'none'}
),
        # Dropdown for selecting stocks 
        dcc.Dropdown(
            id='stock-dropdown',
            options=[{'label': symbol, 'value': symbol} for symbol in stock_data_dict.keys()],
            multi=True,
            value=["XLC",  "XLY",  "XLP", "XLE",  "XLF",  "XLV", "XLI", "XLB",  "XLRE", "XLK",  "XLU"]  # Default selected stocks
        ),

        # Dropdown for selecting plot type 
        dcc.Dropdown(
            id='plot-type-dropdown',
            options=[
                {'label': 'Heatmap', 'value': 'heat'},
                {'label': 'Line Chart', 'value': 'line'},
                {'label': 'Line Chart2', 'value': 'line2'},
            ],
            value='heat'  # Default plot type
        ),

        # Chart display area
        dcc.Graph(id='sector_selected-chart'),

        # Shared text for all charts
        html.Div([
            html.P("Research Question:", style={'fontSize': 30}),
        ]),

        # Unique text for the Bar Chart
        html.Div(id='sector_heat-text', style={'fontSize': 22}),

        # Unique text for the Volatility Chart
        html.Div(id='sector_line-text', style={'fontSize': 22}),

        # Unique text for the Line Chart
        html.Div(id='sector_line2-text', style={'fontSize': 22}),
       
    ])
