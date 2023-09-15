import dash
from dash import dcc, html

def get_layout():
    return html.Div([
        # Content for International/Economic
        html.H2("Economic Indicators and Country Performance"),
        html.P("This page is all about the question: How do different indicators correlate with the stock market performance of countries and can you use the indicators to predict the behaviour?"),
        html.P("""In order to answer this question, the price data of the largest indices of various countries were collected, adjusted and 
                then calculated the average annual growth.
                GDP growth, inflationrate, unemploymentrate and individuals using internet were used as indicators. 
                These are already available on https://data.worldbank.org/ in annual frequency and only had to be parsed.
                A radar plot was then used to see which indicators might be best suited for making predictions."""),
        html.Img(src='assets/radar-plot.png'),
        html.P("""After extensive analysis across several countries, we came to the conclusion that the inflation rate and the unemployment rate were well suited.
                The only problem was that the economic indicators from the radar plot were only available on an annual basis. 
                meaningful overall result, especially since the price data only go back to 2012 and after adjustment there are only 10 data points left. 
                remained.
                As a solution, we used another data source (https://data.oecd.org/), which provides data in monthly frequency.
                For the subsequent analysis, the average monthly growth of the index rate was calculated.
                After normalisation, the data was then plotted."""),
        html.Img(src='assets/correlation1.png'),
        html.Img(src='assets/correlation2.png'),
        html.Img(src='assets/correlation3.png'),
        html.P("""It is noticeable with both indicators that two regimes often form, one high, low inflation and one high, low unemployment rate.
                In order to find out whether one of the indicators has a certain predictive power, we have clustered the two regimes and calculated the average stock performance for each regime.
                calculated the average stock performance for each regime; if it has no predictive power, the two values should be quite close to each other.
                This was also the case with the unemployment rate. So we conclude that the unemployment rate has no predictive power for the performance of the indices.
                (Is this correct, or is it more of a correlation when inflation is low and the share price is high, for example?)
                With the inflation rate the whole thing looks a little different, there are some countries like (insert country) differences of up to
                up to 3%. From this you can infer a strong correlation between stock performance and inflation rate and if you manage to find the inflation rate
                for the current month at the beginning of the month, one could at least have predicted the performance in the past to a certain degree."""),
        #html.Div(id='selected-stock-text', style={'fontSize': 22}),

       
    ])