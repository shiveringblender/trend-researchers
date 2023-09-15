import dash
from dash import dcc, html
import pandas as pd
from data import sector_stock_data_dict as stock_data_dict

def get_layout():
    return html.Div([
        # Content for Event Analysis
        html.H2("Sector Performance Analysis"),
        html.P("Analyzing sectors instead of individual stocks is crucial for understanding general trends in financial markets and developing successful investment strategies.\
        Sectors represent groupings of companies that share similar business areas or industries, such as technology, healthcare, and energy. This concept allows for the\
        aggregation of companies with common business dynamics and economic influencers. The examination of sectors offers a multitude of advantages, including improved \
        diversification, the identification of macroeconomic trends, forecasting market movements, pinpointing opportunities and risks, as well as considering industry\
        developments. Through the following visualizations, we have explored their role as valuable tools for comprehensively analyzing financial markets and optimizing \
        investment decisions."),
        html.P("In 2015 the Global Industry Classification Standard (GICSS) reclassified the former 10 sectors into 11 sectors. This also needs to be \
        considered for the interpretation."),
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
                {'label': 'Sector Closing Prices', 'value': 'line'},
          #      {'label': 'Market Percentage', 'value': 'line2'},
            ],
            value='heat'  # Default plot type
        ),

        # Chart display area
        dcc.Graph(id='sector_selected-chart'),

        # Shared text for all charts
        html.Div([
            html.P("Research Question: How do different sectors (e.g., technology, healthcare, energy) perform relative to each other and the broader market?", style={'fontSize': 30}),
        ]),

        # Unique text for the Bar Chart
        html.Div(id='sector_heat-text'),

        # Unique text for the Volatility Chart
        html.Div(id='sector_line-text'),

        # Unique text for the Line Chart
        html.Div(id='sector_line2-text'),
        html.Img(src='assets/marketperc.png'),
        html.Div([
            html.P("The market percentage, a key metric in financial analysis, provides a comprehensive view of the market's composition by revealing the proportion that each sector holds within the total sum of sector prices. This gives us a deeper look into the performance of individual sectors, as it isolates their relative strength and influence on the broader economic landscape."),
        ]),
       
    ])
