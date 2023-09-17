import dash
from dash import dcc, html
def get_layout():
    return html.Div([
                html.H2("Welcome to the Stock Data Analysis Dashboard by the Group Trend Researchers"),
                html.P("This dashboard allows you to explore various aspects of stock market data and answer different research questions."),
                html.P("Use the tabs above to navigate to different sections of the dashboard."),
                html.P("Our data sources are:"),
                html.A("Yahoo Finance", href="https://de.finance.yahoo.com", target="_blank"),
                html.P(""),
                html.A("Alphavantage", href="https://alphavantage.co", target="_blank"),
                html.P(""),
                html.A("OECD Data", href="https://data.oecd.org/ ", target="_blank"),
                html.P(""),
                html.A("Worldbank Data", href="https://data.worldbank.org/ ", target="_blank"),
                ])