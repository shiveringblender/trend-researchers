import dash
from dash import dcc, html
import pandas as pd
from data import weeklyadj_stock_data_dict as stock_data_dict

def get_layout():
    return html.Div([
        # Content for Event Analysis
        html.H2("Event Analysis"),
        html.P("""We are fetching historical stock data and display information for one year before and after an event or specified
               date. The primary focus is to analyze the effects of significant global events, such as elections or crises, on the stock market. 
               Users can input a target date, and the program retrieves stock data
               for one year before and after the specified date, providing insights into how the event influenced stock prices."""),
        dcc.DatePickerSingle(
        id='event-date-picker',
        date=pd.to_datetime('2020-03-15'),
        display_format='YYYY-MM-DD',
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
        dcc.Graph(id='events_selected-chart'),

        # Shared text for all charts
        html.Div([
            html.P("Research Question: How do specific events (like elections, major geopolitical events, product launches, earnings reports) impact stock prices?\
                    The default date selected is the start of the covid-19 lockdowns but the date can be changed to look at whatever date interests you", style={'fontSize': 30}),
            html.P("Brexit Referendum (2016):  The United Kingdom's decision to leave the European Union had a notable impact on both British and European stocks.\
                   For instance, the stock of British bank hsbc holdings went up significantly in the year after the referendum(23-06-2016). But the same stock also went down a lot after the actual Brexit ( 01-02-2020).", style={'fontSize': 22}),
            html.P("       2016 U.S. Presidential Election: \
                   The election of Donald Trump as the 45th President of the United States was followed by rises in the financial sector.\
                   For example, the stock of Goldman Sachs and JPMorgan went up after the 8th of November 2016, most likely due to the expectation of tax breaks and deregulation, which is part of the republican agenda." , style={'fontSize': 22}), 
            html.P("       Effect of COVID-19 Lockdowns on Stocks: \
                   The start of the COVID-19 pandemic and subsequent lockdowns in early 2020 had a profound and wide-ranging impact on the stock market. It had by far the biggest effect on the broad market of the events we analysed.\
                   Most stocks crashed heavily initially, but most also recovered in the one year after and some even thrived, like Amazon, due to many more people ordering things online due to being confined to their homes."
                   , style={'fontSize': 22})        
        ]),

        # Unique text for the Bar Chart
        html.Div(id='bar-text', style={'fontSize': 22}),

        # Unique text for the Volatility Chart
        html.Div(id='line-text', style={'fontSize': 22}),

        # Unique text for the Line Chart
        html.Div(id='vol-text', style={'fontSize': 22}),

        # Unique text for the Cumulative Returns Chart
        html.Div(id='ret-text', style={'fontSize': 22}),
       
    ])
