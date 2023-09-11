import dash
from dash import dcc, html
import pandas as pd
# Import stock_data_dict 
from data import load_stock_data
stock_data_dict = load_stock_data()

def get_layout():
    return html.Div([
                # Content for Event Analysis
                html.H2("Event Analysis"),
                html.P("Analyze how specific events impact stock prices."),
                # Input for selecting the event date
                dcc.DatePickerSingle(
                    id='event-date-picker',
                    date=pd.to_datetime('2020-03-15'),  # Set the initial event date
                    display_format='YYYY-MM-DD'
                ),
                # Dropdown for selecting stocks 
                dcc.Dropdown(
                    id='stock-dropdown',
                    options=[{'label': symbol, 'value': symbol} for symbol in stock_data_dict.keys()],
                    multi=True,
                    value=['AAPL','AMZN','GOOGL','META','MSFT']  # Default selected stocks
                ),
            
                # Dropdown for selecting plot type 
                dcc.Dropdown(
                    id='plot-type-dropdown',
                    options=[
                        {'label': 'Bar Chart', 'value': 'bar'},
                        {'label': 'Line Chart', 'value': 'line'},
                        {'label': 'Volatility Chart', 'value': 'volatility'},
                        {'label': 'Cumulative Returns Chart', 'value': 'returns'}
                    ],
                    value='bar'  # Default plot type
                ),
            
                # Chart display area
                dcc.Graph(id='selected-chart'),
            
                # Shared text for all charts
                html.Div([
                    html.P("Research Question: How do specific events (like elections, major geopolitical events, product launches, earnings reports) impact stock prices?\
                           The default date selected is the start of the covid-19 lockdowns but the date can be changed to look at whatever date interests you", style={'fontSize': 30}),
                ]),
            
                # Unique text for the Bar Chart
                html.Div(id='bar-chart-text', style={'fontSize': 22}),
            
                # Unique text for the Volatility Chart
                html.Div(id='volatility-chart-text', style={'fontSize': 22}),
            
                # Unique text for the Line Chart
                html.Div(id='line-chart-text', style={'fontSize': 22}),
            
                # Unique text for the Cumulative Returns Chart
                html.Div(id='returns-chart-text', style={'fontSize': 22}),
           
            ])