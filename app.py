import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
# Import layout and callbacks for each tab
from tabs.events import layout as events_layout
from tabs.events import callbacks as events_callbacks
# from tabs.correlation import layout as correlation_layout
# from tabs.correlation import callbacks as correlation_callbacks
# from tabs.economic import layout as economic_layout
# from tabs.economic import callbacks as economic_callbacks
from tabs.international_economic import layout as international_economic_layout
from tabs.international_economic import callbacks as international_economic_callbacks
from tabs.economic_factors import layout as economic_factors_layout
from tabs.economic_factors import callbacks as economic_factors_callbacks
from tabs.sector_performance import layout as sector_performance_layout
from tabs.sector_performance import callbacks as sector_performance_callbacks
from tabs.sentiment import layout as sentiment_layout
from tabs.sentiment import callbacks as sentiment_callbacks
from tabs.home import layout as home_layout
from tabs.home import callbacks as home_callbacks
from tabs.predict import layout as predict_layout
from tabs.predict import callbacks as predict_callbacks



# Initialize the Dash app
app = dash.Dash(__name__,suppress_callback_exceptions=True)
server = app.server


    
# Define the layout of the app
app.layout = html.Div([
    html.H1("Stock Data Analysis Dashboard"),

    dcc.Tabs(id="tabs", value='home', children=[
         dcc.Tab(label='Home', value='home'),
         dcc.Tab(label='Correlation Analysis', value='correlation'),
         dcc.Tab(label='International Correlation and Economic Indicators', value='international_economic'),
         dcc.Tab(label='Sentiment Analysis', value='sentiment'),
         dcc.Tab(label='Sector Performance', value='sector_performance'),
         dcc.Tab(label='Economic Factors', value='economic_factors'),
         dcc.Tab(label='Event Analysis', value='event_analysis' ),
         dcc.Tab(label='Prediction', value = 'predict')
    ]),

    html.Div(id='tab-content'),
])




# Define callback to update the content of the selected tab
@app.callback(
    Output('tab-content', 'children'),
    Input('tabs', 'value'),
)

def render_content(tab):
    if tab == 'home':
        return home_layout.get_layout()
    # elif tab == 'correlation':
    #     return correlation_layout.get_layout()
    elif tab == 'international_economic':
         return international_economic_layout.get_layout()
    elif tab == 'sentiment':
         return sentiment_layout.get_layout()
    elif tab == 'sector_performance':
        return sector_performance_layout.get_layout()
    elif tab == 'economic_factors':
         return economic_factors_layout.get_layout()
    elif tab == 'event_analysis':
        return events_layout.get_layout()
    elif tab == 'predict':
        return predict_layout.get_layout()
    else:
        return html.Div([]) 


@app.callback(
    Output('sector_selected-chart', 'figure'),
    Output('sector_heat-text', 'children'),
    Output('sector_line-text', 'children'),
    Output('sector_line2-text', 'children'),
    Input('stock-dropdown', 'value'),
    Input('plot-type-dropdown', 'value'),
    State('tabs', 'value')
)
def update_sector_performance_chart(selected_stocks, plot_type, tab):
    if tab == 'sector_performance':
        # Call the relevant function to update the sector_performance tab components
        return sector_performance_callbacks.update_chart(selected_stocks, plot_type)
    else:
        return {}, "", "", "", ""
    
@app.callback(
    Output('events_selected-chart', 'figure'),
    Output('bar-text', 'children'),
    Output('line-text', 'children'),
    Output('vol-text', 'children'),
    Output('ret-text', 'children'),
    Input('stock-dropdown', 'value'),
    Input('plot-type-dropdown', 'value'),
    
    Input('event-date-picker', 'date'),
    State('tabs', 'value')
)
def update_event_analysis_chart(selected_stocks, plot_type, event_date, tab):
    if tab == 'event_analysis':
        # Call the relevant function to update the event_analysis tab components
        return events_callbacks.update_chart(selected_stocks, plot_type, event_date)
    else:
        return {}, "", "", "", ""

@app.callback(
    Output('stock-price-graph', 'figure'),    
    Output('selected-stock-text', 'children'),
    Input('nasdaq-dropdown', 'value'),
    Input('start-date-picker', 'date'),
    Input('end-date-picker', 'date'),
    Input('train-button', 'n_clicks'),
    Input('future-button', 'n_clicks'),
    State('tabs', 'value')
)
def update_predict_chart(selected_stock, start_date, end_date,train_click,future, tab):
    if tab =='predict':
        return predict_callbacks.update_chart( selected_stock, start_date, end_date, train_click, future)
    else:
        return ""
    

@app.callback(
    Output('sentiment-graph', 'figure'),
    Input('days-dropdown', 'value'),
    State('tabs', 'value')
)
def update_sentiment_chart(days, tab):
    if tab =='sentiment':
        return sentiment_callbacks.update_chart(days)
    else:
        return {} 
    
@app.callback(
    Output('smp-chart', 'figure'),
    Input('us-dropdown','value'),
    State('tabs', 'value')
)
def update_economic_factors_chart(selected_charts, tab):
    if tab =='economic_factors':
        return economic_factors_callbacks.update_chart(selected_charts)
    else:
        return {} 


if __name__ == '__main__':
    app.run_server(debug=True)
