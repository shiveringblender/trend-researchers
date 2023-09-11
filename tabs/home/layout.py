import dash
from dash import dcc, html
def get_layout():
    return html.Div([
                html.H2("Welcome to the Stock Data Analysis Dashboard by the Group Trend Researchers", style={'fontSize': 30}),
                html.P("This dashboard allows you to explore various aspects of stock market data and answer different research questions.",style={'fontSize': 22}),
                html.P("Use the tabs above to navigate to different sections of the dashboard.",style={'fontSize': 22}),
                ])