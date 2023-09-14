import dash
from dash import dcc, html
import pandas as pd

def get_layout():
    return html.Div([
        # Content for Sentiment Analysis
        html.H2("Sentiment Analysis"),
        html.P(""),

        dcc.Dropdown(
            id='days-dropdown',
            options=[{'label': str(day), 'value': day} for day in [21,22,23,24,25]],
            multi=True,
            placeholder="Select days to look at",
            value = [21,22,23,24,25],
        ),

        dcc.Graph(id='sentiment-graph'),

        

       
    ])