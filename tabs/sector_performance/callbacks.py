import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from data import sector_stock_data_dict
from data import sector_names
from data import spy_data

#line plot method

def line_plot(data_dict, symbols_to_include, sector_names, title):
    event_date = pd.to_datetime('2015-11-11')
    traces = []
    shapes = []  # Add shapes for vertical line
    shapes.append({
        'type': 'line',
        'x0': event_date,
        'x1': event_date,
        'y0': 0,
        'y1': 1,
        'xref': 'x',
        'yref': 'paper',
        'line': {'color': 'red', 'dash': 'dash'},
        'name': 'Reclassification'
    })

    for symbol in symbols_to_include:
        if symbol in data_dict and symbol in sector_names:
            data = data_dict[symbol]
            sector_name = sector_names[symbol]
            trace = go.Scatter(
                x=data.index,
                y=data['value'],
                mode='lines',
                name=sector_name  # Use the sector name as the trace name
            )
            traces.append(trace)

    figure = {
        'data': traces,
        'layout': {
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Market Percentage'},
            'showlegend': True,
            'legend': dict(
                orientation="h",
                entrywidth=150,
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            'shapes': shapes,
            'title': title  # Set the title of the plot
        }
    }

    fig = go.Figure(figure)
    return fig
    
def heatmap_sectors(sector_stock_data_dict, sector_names, symbols_to_include):
    # Create a DataFrame with the selected symbols
    selected_data = [sector_stock_data_dict[symbol]["value"] for symbol in symbols_to_include]
    combined_df = pd.concat(selected_data, axis=1)
    combined_df.columns = [sector_names[symbol] for symbol in symbols_to_include]

    # Calculate the correlation matrix
    df_corr = combined_df.corr()  # Generate correlation matrix

    fig = go.Figure()
    fig.add_trace(
        go.Heatmap(
            x=df_corr.columns,
            y=df_corr.index,
            z=np.array(df_corr),
            hoverongaps=False
        )
    )
    return fig
    
def update_chart(selected_sectors, plot_type):
    if plot_type == 'heat':
        return heatmap_sectors(sector_stock_data_dict, sector_names, selected_sectors),"","",""
            
    elif plot_type == 'line': 
        return line_plot(sector_stock_data_dict,selected_sectors,sector_names, "adfas"),"","",""
    else:
        return {}, "", "", ""
           
