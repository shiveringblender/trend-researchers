import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from data import smp_data_dict as data_dict

def plot_time_series_with_events(selected_chart):
    # Define events
    events = [{"name": "2008 Financial Crisis", "date": "2008-09-15"},
              {"name": "First COVID-19 Pandemic Lockdowns", "date": "2020-03-11"}]

    # Check if the selected symbol is in the data_dict
    if selected_chart in data_dict:
        df = data_dict[selected_chart]

        # Create a Plotly figure
        fig = go.Figure()

        # Add a line plot for the time series data
        fig.add_trace(go.Scatter(x=df.index, y=df["value"], mode="lines", name=selected_chart))

        # Add vertical lines for events
        for event in events:
            fig.add_shape(go.layout.Shape(
                type="line",
                x0=event["date"],
                x1=event["date"],
                y0=0,
                y1=1,
                yref="paper",
                line=dict(color="red", dash="dash"),
                name=event["name"]
            ))
            fig.add_annotation(
                x=event["date"],
                y=1.02, 
                text=event["name"],
                showarrow=False,
                xref="x",
                yref="paper",
                font=dict(color="red")  
            )

        # Set the title and labels
        fig.update_layout(
            title=f"{selected_chart} Time Series with Events",
            xaxis_title="Date",
            yaxis_title=selected_chart,
            showlegend=True
        )

        return fig

# Define function to update the chart
def update_chart(selected_chart):
    return plot_time_series_with_events(selected_chart)
