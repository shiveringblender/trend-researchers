import dash
from dash import dcc, html

def get_layout():
    return html.Div([
        # Content for International/Economic
        html.H2("Economic Indicators and Country Performance"),
        html.P(
            "This page focuses on the question: How do different indicators "
            "correlate with the stock market performance of countries, and "
            "can you use the indicators to predict behavior?"
        ),
        html.P(
            "To answer this question, we collected and adjusted price data "
            "for the largest indices of various countries, calculating the "
            "average annual growth. Indicators like GDP growth, inflation "
            "rate, unemployment rate, and internet usage were used. These "
            "are available on https://data.worldbank.org/ annually and "
            "required parsing. We used a radar plot to identify the best "
            "prediction indicators."
        ),
        html.Img(src="assets/radar-plot.png"),
        html.P(
            "After extensive analysis across several countries, we concluded "
            "that inflation rate and unemployment rate were suitable. "
            "However, economic indicators from the radar plot were only "
            "available annually, limiting meaningful results, especially "
            "since price data only go back to 2012, leaving only 10 data "
            "points. We used another data source (https://data.oecd.org/) "
            "providing monthly data. We calculated the average monthly "
            "growth of the index rate for subsequent analysis, normalized "
            "the data, and plotted it."
        ),
        html.Img(src="assets/correlation1.png", style={"max-width":"100%"}),
        html.Img(src="assets/correlation2.png", style={"max-width":"100%"}),
        html.Img(src="assets/correlation3.png", style={"max-width":"100%"}),
        html.P(
            "It is noticeable that both indicators often result in two "
            "regimes: one with high inflation and low unemployment, and the "
            "other with low inflation and high unemployment. To determine "
            "their predictive power, we clustered these regimes and "
            "calculated the average stock performance for each. If the "
            "indicators lack predictive power, the values should be close. "
            "This was the case with unemployment rate, suggesting it lacks "
            "predictive power. However, the situation differs with inflation "
            "rate; some countries show differences up to 3%. This implies a "
            "strong correlation between stock performance and inflation rate. "
            "Predicting past performance could be feasible if one can obtain "
            "inflation rates at the start of each month."
        ),
    ])
