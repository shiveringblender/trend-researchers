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
            options=[{'label': str(day), 'value': day}
                     for day in [21, 22, 23, 24, 25]],
            multi=True,
            placeholder="Select days to look at",
            value=[21, 22, 23, 24, 25],
        ),

        dcc.Graph(id='sentiment-graph'),

        # Shared text for all charts
        html.Div([
            html.P("Research Question: Does public sentiment measured by news articles and tweets about a company have any predictive power for stock prices?", style={
                   'fontSize': 30}),
            html.P("In this section, I also examined the effect of public sentiment on Nvidia stock.\
                    We have collected newsletter articles, in which the share name of Nvidia occurred\
                    in the period from 21.08.2023 - 25.08.2023 and then stored the sentiment score and\
                    the publication time for each article. The sentiment score was a value between -1 \
                   and 1, where -1 indicates distrust and 1 euphoric. For Nvidia, we have also stored\
                    the stock price in the period from 21.08.2023 - 25.08.2023 in the interval of 5 min.\
                    The time period was chosen deliberately. Nvidia has disclosed its results on\
                    23.08.2023 and expectations were very high. Therefore, the effect of the\
                    expectations can be examined particularly well here. We have now adjusted both data\
                    sets to each other, normalized them and packed them together in a plot.\
                    The result can be seen in the figure above. If you compare the sentiment line with\
                    the stock price line, you will immediately notice the similarity. Especially after\
                    a timeshift, the course is enormously similar and the two lines have a Pearson\
                    Correlation Coeffiecient Value of 0.6. From this, one can deduce that public\
                    sentiment is definitely a variable that can be used to predict future changes in\
                    a stock price."),
            html.P("But the problem is the following: If high expectations are not met,\
                the stock price falls. And it is not possible to predict whether expectations\
                will be met. In our example with Nvidia, however, they were met and then\
                public sentiment is a means of predicting the stock price."),
        ]),
    ])
