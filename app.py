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
# from tabs.international import layout as international_layout
# from tabs.international import callbacks as international_callbacks
# from tabs.sector_indicator import layout as sector_indicator_layout
# from tabs.sector_indicator import callbacks as sector_indicator_callbacks
from tabs.sector_performance import layout as sector_performance_layout
from tabs.sector_performance import callbacks as sector_performance_callbacks
# from tabs.sentiment import layout as sentiment_layout
# from tabs.sentiment import callbacks as sentiment_callbacks
from tabs.home import layout as home_layout
from tabs.home import callbacks as home_callbacks




# Initialize the Dash app
app = dash.Dash(__name__,suppress_callback_exceptions=True)
server = app.server


    
# Define the layout of the app
app.layout = html.Div([
    html.H1("Stock Data Analysis Dashboard"),

    dcc.Tabs(id="tabs", value='home', children=[
         dcc.Tab(label='Home', value='home'),
         dcc.Tab(label='Correlation Analysis', value='correlation'),
         dcc.Tab(label='Economic Indicators', value='economic'),
         dcc.Tab(label='International Correlation', value='international'),
         dcc.Tab(label='Sentiment Analysis', value='sentiment'),
         dcc.Tab(label='Sector Performance', value='sector_performance'),
         dcc.Tab(label='Sector Indicator', value='sector_indicator'),
         dcc.Tab(label='Event Analysis', value='event_analysis' ),
                   
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
    # elif tab == 'economic':
    #     return economic_layout.get_layout()
    # elif tab == 'international':
    #     return international_layout.get_layout()
    # elif tab == 'sentiment':
    #     return sentiment_layout.get_layout()
    elif tab == 'sector_performance':
        return sector_performance_layout.get_layout()
    # elif tab == 'sector_indicator':
    #     return sector_indicator_layout.get_layout()
    elif tab == 'event_analysis':
        return events_layout.get_layout()
    else:
        return html.Div([]) 


# @app.callback(
#     Output('selected-chart', 'figure'),
#     Output('chart1-text', 'children'),
#     Output('chart2-text', 'children'),
#     Output('chart3-text', 'children'),
#     Output('chart4-text', 'children'),
#     Input('stock-dropdown', 'value'),
#     Input('plot-type-dropdown', 'value'),
#     Input('event-date-picker', 'date'),
#     State('tabs', 'value')
# )
# def update_home_chart(selected_stocks, plot_type, event_date, tab):
#     if tab == 'home':
#         # Call the relevant function to update the home tab components
#         return home_callbacks.update_chart(selected_stocks, plot_type, event_date)
#     else:
#         return {}, "", "", "", ""
    
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

# @app.callback(
#     Output('selected-chart', 'figure'),
#     Output('chart1-text', 'children'),
#     Output('chart2-text', 'children'),
#     Output('chart3-text', 'children'),
#     Output('chart4-text', 'children'),
#     Input('stock-dropdown', 'value'),
#     Input('plot-type-dropdown', 'value'),
#     Input('event-date-picker', 'date'),
#     State('tabs', 'value')
# )
# def update_event_analysis_chart(selected_stocks, plot_type, event_date, tab):
#     if tab == 'event_analysis':
#         # Call the relevant function to update the event_analysis tab components
#         return events_callbacks.update_chart(selected_stocks, plot_type, event_date)
#     else:
#         return {}, "", "", "", ""
    
# @app.callback(
#     Output('selected-chart', 'figure'),
#     Output('chart1-text', 'children'),
#     Output('chart2-text', 'children'),
#     Output('chart3-text', 'children'),
#     Output('chart4-text', 'children'),
#     Input('stock-dropdown', 'value'),
#     Input('plot-type-dropdown', 'value'),
#     Input('event-date-picker', 'date'),
#     State('tabs', 'value')
# )
# def update_event_analysis_chart(selected_stocks, plot_type, event_date, tab):
#     if tab == 'event_analysis':
#         # Call the relevant function to update the event_analysis tab components
#         return events_callbacks.update_chart(selected_stocks, plot_type, event_date)
#     else:
#         return {}, "", "", "", ""
if __name__ == '__main__':
    app.run_server(debug=True)
