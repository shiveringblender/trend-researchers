import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from data import sentimentdf

def update_chart(days):
    date_df = pd.DataFrame({'day': days, 'month': 8, 'year': 2023})
    date_df['date'] = pd.to_datetime(date_df[['year', 'month', 'day']])
    days = date_df['date'].dt.strftime('%Y-%m-%d').tolist()
    print(days)
    filtered_data = sentimentdf[sentimentdf["Date"].dt.strftime('%Y-%m-%d').isin(days)]

    trace1 = go.Scatter(
        x=filtered_data["Date"],
        y=filtered_data["4. close_smoothed"],
        mode='lines',
        name='Nvidia Stock Price'
    )

    trace2 = go.Scatter(
        x=filtered_data["Date"],
        y=filtered_data["ticker_sentiment_smoothed"],
        mode='lines',
        name='Sentiment'
    )

    trace3 = go.Scatter(
        x=filtered_data["Date"],
        y=filtered_data["ticker_sentiment_smoothed_shifted"],
        mode='lines',
        name='Sentiment Shifted'
    )


    fig = go.Figure(data=[trace1, trace2, trace3])

    return fig