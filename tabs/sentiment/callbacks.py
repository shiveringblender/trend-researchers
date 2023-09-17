import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from data import sentimentdf


def update_chart(days):
    # Create a DataFrame with day, month, and year columns
    date_df = pd.DataFrame({"day": days, "month": 8, "year": 2023})

    # Combine year, month, and day columns to create a 'date' column
    date_df["date"] = pd.to_datetime(date_df[["year", "month", "day"]])

    # Convert dates to a list of strings in "YYYY-MM-DD" format
    days = date_df["date"].dt.strftime("%Y-%m-%d").tolist()
    print(days)

    # Filter sentiment data based on the selected dates
    filtered_data = sentimentdf[sentimentdf["Date"].dt.strftime(
        "%Y-%m-%d").isin(days)]

    # Create trace1 for Nvidia stock price
    trace1 = go.Scatter(
        x=filtered_data["Date"],
        y=filtered_data["4. close_smoothed"],
        mode="lines",
        name="Nvidia Stock Price"
    )

    # Create trace2 for sentiment data
    trace2 = go.Scatter(
        x=filtered_data["Date"],
        y=filtered_data["ticker_sentiment_smoothed"],
        mode="lines",
        name="Sentiment"
    )

    # Create trace3 for shifted sentiment data
    trace3 = go.Scatter(
        x=filtered_data["Date"],
        y=filtered_data["ticker_sentiment_smoothed_shifted"],
        mode="lines",
        name="Sentiment Shifted"
    )

    # Create a plotly figure with the traces
    fig = go.Figure(data=[trace1, trace2, trace3])

    # Update the layout of the figure
    fig.update_layout(
        title="Public Sentiment impacts Stock Price",
        xaxis_title="Date",
        yaxis_title="Normalized Value"
    )

    return fig
