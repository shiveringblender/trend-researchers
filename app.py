import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Stock data

stock_symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN','NVDA','TSLA','META','HSBC','TSM','XOM','JNJ']
window_size = 52
stock_data_dict = {}
avg_price_before_event_dict = {}
avg_price_after_event_dict = {}
std_dev_before_event_dict = {}
std_dev_after_event_dict = {}
csv_folder = 'csv_data_events'
csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]
for csv_file in csv_files:
    # Extract the symbol from the CSV filename (assuming the filename format is "{symbol}_data.csv")
    symbol = os.path.splitext(csv_file)[0].split('_')[0]
    
    # Load the CSV data into a DataFrame
    data = pd.read_csv(os.path.join(csv_folder, csv_file), index_col=0, parse_dates=True)
    
    # Store the data in stock_data_dict with the symbol as the key
    stock_data_dict[symbol] = data

# Function to calculate average prices and standard deviations
def calculate_metrics(data, event_date):
    avg_price_before_event = data[data.index < event_date]['5. adjusted close'].mean()
    std_dev_before_event = data[data.index < event_date]['5. adjusted close'].std()
    
    avg_price_after_event = data[data.index >= event_date]['5. adjusted close'].mean()
    std_dev_after_event = data[data.index >= event_date]['5. adjusted close'].std()
    
    return {
        'avg_price_before_event': avg_price_before_event,
        'std_dev_before_event': std_dev_before_event,
        'avg_price_after_event': avg_price_after_event,
        'std_dev_after_event': std_dev_after_event
    }

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Define the layout of the app
app.layout = html.Div([
    html.H1("Stock Data Visualization"),
    
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Event Data', value='tab-1'),
        dcc.Tab(label='Topic 2', value='tab-2'),  # Add more tabs for different topics
        dcc.Tab(label='Topic 3', value='tab-3'),  # Add more tabs for different topics
    ]),
    
    html.Div(id='tab-content'),
])

# Define callback to update the content of the selected tab
@app.callback(
    Output('tab-content', 'children'),
    Input('tabs', 'value')
)
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
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
                value=['AAPL']  # Default selected stocks
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
                html.P("This is some shared text for all charts in this tab.", style={'fontSize': 18}),
            ]),
            
            # Unique text for the Bar Chart
            html.Div(id='bar-chart-text', style={'fontSize': 18}),
            
            # Unique text for the Volatility Chart
            html.Div(id='volatility-chart-text', style={'fontSize': 18}),
            
            # Unique text for the Line Chart
            html.Div(id='line-chart-text', style={'fontSize': 18}),
            
            # Unique text for the Cumulative Returns Chart
            html.Div(id='returns-chart-text', style={'fontSize': 18}),
           
        ])
            
    elif tab == 'tab-2':
        return html.Div([
            # Content for Topic 2
        ])
    elif tab == 'tab-3':
        return html.Div([
            # Content for Topic 3
        ])
    else:
        return html.Div([])  # Handle unsupported tabs

# Define callback to update the graph based on user selections
@app.callback(
    Output('selected-chart', 'figure'),
    Output('bar-chart-text', 'children'),
    Output('volatility-chart-text', 'children'),
    Output('line-chart-text', 'children'),
    Output('returns-chart-text', 'children'),
    Input('stock-dropdown', 'value'),
    Input('plot-type-dropdown', 'value'),
    Input('event-date-picker', 'date')
)

def update_chart(selected_stocks, plot_type, selected_event_date):
    event_date = pd.to_datetime('2020-03-15')
    if selected_event_date:
        event_date = pd.to_datetime(selected_event_date)
    # Filter the data to consider only one year before and after the selected event date
    date_one_year_before = event_date - pd.DateOffset(years=1)
    date_one_year_after = event_date + pd.DateOffset(years=1)
    chart_data = []
    
    if plot_type == 'bar':
        traces = []
        x_values = []
        before_values = []
        after_values = []

        for stock_symbol in selected_stocks:
            data = stock_data_dict[stock_symbol]
            # Filter data for one year before and after the event date
            filtered_data = data[(data.index >= date_one_year_before) & (data.index <= date_one_year_after)]
            # Calculate average prices before and after the event date
            metrics = calculate_metrics(filtered_data, event_date)
            avg_price_before = metrics['avg_price_before_event']
            avg_price_after = metrics['avg_price_after_event']

            x_values.append(stock_symbol)
            before_values.append(avg_price_before)
            after_values.append(avg_price_after)

        traces.append({
            'x': x_values,
            'y': before_values,
            'name': 'Before Event',
            'type': 'bar',
            'marker': {'color': 'blue'},
        })

        traces.append({
            'x': x_values,
            'y': after_values,
            'name': 'After Event',
            'type': 'bar',
            'marker': {'color': 'orange'},
        })
        
        figure = {
            'data': traces,
            'layout': {
                'barmode': 'group', 
                'bargap': 0.2,
                'title': f'Average Adjusted Closing Price Before and After Event',
                'xaxis': {'title': 'Company'},
                'yaxis': {'title': 'Average Adjusted Closing Price ($)'}
            }
        }
        bar_chart_text = "This is unique text for the Bar Chart."
        return figure, bar_chart_text, "", "", ""
    elif plot_type == 'line':
        # Create a Plotly line chart
        traces = []
        shapes = []  # Add shapes for vertical line
        for stock_symbol in selected_stocks:
            data = stock_data_dict[stock_symbol]
            filtered_data = data[(data.index >= date_one_year_before) & (data.index <= date_one_year_after)]
            # Create a scatter trace for each stock
            trace = go.Scatter(
                x=filtered_data.index,
                y=filtered_data['5. adjusted close'],
                mode='lines',
                name=stock_symbol
            )
            traces.append(trace)

        # Add vertical line for event date
        shapes.append({
            'type': 'line',
            'x0': event_date,
            'x1': event_date,
            'y0': 0,
            'y1': 1,
            'xref': 'x',
            'yref': 'paper',
            'line': {'color': 'red', 'dash': 'dash'},
            'name': 'Event Date'
        })

        figure = {
            'data': traces,
            'layout': {
                'title': 'Historical Stock Prices (One Year Before and After Event)',
                'xaxis': {'title': 'Date'},
                'yaxis': {'title': 'Adjusted Closing Price ($)'},
                'showlegend': True,
                'legend': {'x': 0, 'y': 1},
                'shapes': shapes  # Include the shapes for vertical line
            }
        }
        line_chart_text = "This is unique text for the Line Chart."
        return figure, "", "", line_chart_text, ""
    
    elif plot_type == 'volatility':
        # Create a Plotly volatility chart for selected stocks
        traces = []
        shapes = []

        for stock_symbol in selected_stocks:
            data = stock_data_dict[stock_symbol]
            filtered_data = data[(data.index >= date_one_year_before) & (data.index <= date_one_year_after)]
            std_dev = filtered_data['5. adjusted close'].rolling(window=window_size, min_periods=1).std()
            
            # Create a scatter trace for each stock's volatility
            trace = go.Scatter(
                x=filtered_data.index,
                y=std_dev,
                mode='lines',
                name=f'{stock_symbol} Std. Dev.'
            )
            traces.append(trace)

        # Add vertical line for event date
        shapes.append({
            'type': 'line',
            'x0': event_date,
            'x1': event_date,
            'y0': 0,
            'y1': 1,
            'xref': 'x',
            'yref': 'paper',
            'line': {'color': 'red', 'dash': 'dash'},
            'name': 'Event Date'
        })

        figure = {
            'data': traces,
            'layout': {
                'title': 'Price Volatility Before and After Event',
                'xaxis': {'title': 'Date'},
                'yaxis': {'title': 'Standard Deviation of Adjusted Close Price'},
                'showlegend': True,
                'legend': {'x': 0, 'y': 1},
                'shapes': shapes  # Include the shapes for vertical line
            }
        }
        volatility_chart_text = "This is unique text for the Volatility Chart."
        return figure, "", volatility_chart_text, "", ""
    
    elif plot_type == 'returns':
        # Create a Plotly volatility chart
        traces = []
        for stock_symbol in selected_stocks:
            data = stock_data_dict[stock_symbol]
            filtered_data = data[(data.index >= date_one_year_before) & (data.index <= date_one_year_after)]
            returns = (filtered_data['5. adjusted close'] / filtered_data['5. adjusted close'].iloc[0] - 1) * 100
            # Create a scatter trace for each stock's cumulative returns
            trace = go.Scatter(
                x=filtered_data.index,
                y=returns,
                mode='lines',
                name=f'{stock_symbol} Cumulative Returns'
            )
            traces.append(trace)

        # Add vertical line for event date
        shapes = [{
            'type': 'line',
            'x0': event_date,
            'x1': event_date,
            'y0': 0,
            'y1': 1,
            'xref': 'x',
            'yref': 'paper',
            'line': {'color': 'red', 'dash': 'dash'},
            'name': 'Event Date'
        }]

        figure = {
            'data': traces,
            'layout': {
                'title': 'Cumulative Returns Before and After Event',
                'xaxis': {'title': 'Date'},
                'yaxis': {'title': 'Cumulative Returns (%)'},
                'showlegend': True,
                'legend': {'x': 0, 'y': 1},
                'shapes': shapes  # Include the shapes for vertical line
            }
        }
        returns_chart_text = "This is unique text for the Cumulative Returns Chart."
        return figure, "", "", "", returns_chart_text
    else:
        # Handle unsupported plot types
        return {}, "", "", "", ""
    

if __name__ == '__main__':
    app.run_server(debug=True)