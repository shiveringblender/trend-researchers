import dash
from dash import dcc, html
import pandas as pd

# Dictionary of sector symbols and names
symbol_data = {
    'GDP' : {'name': "US Gross domestic product", 'title': 'US Gross domestic product', 'unit': 'billions of US-Dollars'},
    'SPY' : {'name': "S&P500 stock index", 'title': 'S&P500 stock index monthly adjusted closing prices', 'unit': 'Closing price in US-Dollars'},
    'UEM' : {'name': "US Unemploymentrate", 'title': 'US Unemploymentrate', 'unit': 'percent'},
    'INF' : {'name': "US Inflation", 'title': 'US Inflation', 'unit': 'percent'}
}

def get_layout():
    return html.Div([
                # Content for Event Analysis
                html.H2("Economic Indicators"),
                # Dropdown for selecting stocks 
                dcc.Dropdown(
                    id='us-dropdown',
                    options=[{'label': symbol_data[symbol]['name'], 'value': symbol} for symbol in list(symbol_data.keys())],
                    multi=False,
                    value='GDP'
                      # Default selected stocks
                ),
            
                # Chart display area
                dcc.Graph(id='smp-chart'),
            
                # Shared text for all charts
                html.Div([
                    html.P("Research Question: How does stock market performance relate to broader economic indicators like GDP growth, unemployment rates, or inflation rates?"),
                    html.P("In recent decades, the stock market, specifically the S&P 500 index, has emerged as a pivotal barometer of economic health in the US,\
                    reflecting and influencing the nation's financial well-being. This research inquiry aims to meticulously investigate the intricate interplay \
                    between S&P 500 stock market performance and key economic indicators. These indicators encompass fundamental metrics such as Gross Domestic Product (GDP) growth\
                    , unemployment rates, and inflation rates. Understanding the backdrop and significance of these economic indicators is crucial for comprehending their mutual influence on the S&P 500 index and the broader\
                    economic landscape. \n 1. Gross Domestic Product (GDP) Growth: GDP is a fundamental indicator that quantifies the overall economic output of a nation. Examining its relationship \
                    with the S&P 500 stock market index can elucidate how corporate earnings and economic expansion are interlinked. A rising GDP typically suggests a healthy economy, potentially driving\
                    investor confidence and influencing the performance of the S&P 500. \n 2. Unemployment Rates: The unemployment rate reflects the percentage of the labor force without employment and actively\
                    seeking work. High unemployment rates may correlate with reduced consumer spending and corporate profitability, potentially affecting the S&P 500 index. Conversely, low unemployment rates often\
                    indicate economic prosperity, which can buoy investor sentiment and the performance of the S&P 500. \n 3. Inflation Rates: Inflation rates represent the rate at which the general price level of goods\
                    and services rises, resulting in a decrease in the purchasing power of a currency. Fluctuations in inflation can have varying effects on the S&P 500 index, as higher inflation may erode the real returns\
                    on investments, affecting investor decisions and stock prices within the index. \n The economic indicator data was as well as the S&P500 data collected over the Alpha Vantage  API, but those are originally \
                    collected from the Federal Reserve Bank of St. Louis API."),
                ]),
            
                # Unique text for the Line Prices Chart
                html.Div(id='line_symbol_text')
           
            ])