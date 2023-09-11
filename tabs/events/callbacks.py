import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objects as go


from data import stock_data_dict
from app import app

# Function to calculate average prices and standard deviations
def calculate_metrics(data, event_date):
    avg_price_before_event_dict = {}
    avg_price_after_event_dict = {}
    std_dev_before_event_dict = {}
    std_dev_after_event_dict = {}
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

# Callback to update the chart and text based on user selections
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
            filtered_data = data[(data.index >= date_one_year_before) & (data.index <= date_one_year_after)]
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
        bar_chart_text = "The Bar Chart displays the average adjusted closing prices of selected stocks one year before and after a specified event date. It provides a visual comparison of how stock prices changed around the event."
        return figure, bar_chart_text, "", "", ""
    elif plot_type == 'line':
        traces = []
        shapes = []  # Add shapes for vertical line
        for stock_symbol in selected_stocks:
            data = stock_data_dict[stock_symbol]
            filtered_data = data[(data.index >= date_one_year_before) & (data.index <= date_one_year_after)]
            trace = go.Scatter(
                x=filtered_data.index,
                y=filtered_data['5. adjusted close'],
                mode='lines',
                name=stock_symbol
            )
            traces.append(trace)

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
                'shapes': shapes
            }
        }
        line_chart_text = "The Line Chart shows the historical adjusted closing prices of selected stocks over one year before and after the specified event date. It helps visualize the stock price trends leading up to and following the event."
        return figure, "", "", line_chart_text, ""
    elif plot_type == 'volatility':
        # Create a Plotly volatility chart for selected stocks
        traces = []
        shapes = []

        for stock_symbol in selected_stocks:
            data = stock_data_dict[stock_symbol]
            filtered_data = data[(data.index >= date_one_year_before) & (data.index <= date_one_year_after)]
            std_dev = filtered_data['5. adjusted close'].rolling(window=52, min_periods=1).std()
            
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
        volatility_chart_text = "The Volatility Chart illustrates the standard deviation of adjusted closing prices for selected stocks before and after the event. It indicates the level of price volatility in the stock market during this period."
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
        returns_chart_text = "The Cumulative Returns Chart displays the cumulative returns of selected stocks over one year before and after the event. It helps assess the overall performance and growth of the stocks relative to their initial values."
        return figure, "", "", "", returns_chart_text
    else:
        return {}, "", "", "", ""