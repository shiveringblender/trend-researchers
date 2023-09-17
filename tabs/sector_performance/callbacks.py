import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from data import sector_stock_data_dict
from data import sector_names

heatsectortext = (
    "Over all, the correlation between the sectors is quite high. If you take a closer look, you can see the following: "
    "Strong Positive Correlations: The sectors XLY (Consumer Discretionary), XLP (Consumer Staples), XLV (Health Care), "
    "XLI (Industrials), and XLB (Materials) all exhibit strong positive correlations. This means that they tend to rise "
    "or fall simultaneously. This could suggest that they are subject to similar macroeconomic influences or that "
    "investors perceive them similarly. \n"
    "Highest Correlation with XLB: The sector XLB (Materials) has the highest average correlation with the other sectors "
    "in this analysis. This indicates that XLB generally has a strong relationship with other sectors and may potentially "
    "serve as an indicator of broader market trends. \n"
    "Low Correlation with XLE: The energy sector (XLE) generally displays low correlations with most other sectors. This "
    "could be attributed to the unique influences driving the energy sector, such as crude oil prices and geopolitical factors. \n"
    "XLC (Communication Services) as an Outlier: The sector XLC (Communication Services) has a moderate correlation with most "
    "sectors but a low correlation with the energy sector (XLE). This could be attributed to specific factors affecting the "
    "communications industry, such as technological developments and corporate news."
)
sectorclosetext = (
    "As you can see, the prices of all sectors have risen over time, but in the last decade the difference between them has "
    "grown. For example, the financial sector's price rose very slowly and the technology sector quite quickly. In November "
    "2015 the difference between those two sector prices was around $57, and in August 2023 it was $140."
)

def line_plot(data_dict, symbols_to_include, sector_names, title):
    """
    Create a line plot of sector closing prices over time.

    Parameters:
    - data_dict: A dictionary containing sector data.
    - symbols_to_include: A list of sector symbols to include in the plot.
    - sector_names: A dictionary mapping sector symbols to sector names.
    - title: The title of the plot.

    Returns:
    - fig: The Plotly figure object.
    """
    event_date = pd.to_datetime("2015-11-11")
    traces = []
    shapes = []  # Add shapes for vertical line
    shapes.append({
        "type": "line",
        "x0": event_date,
        "x1": event_date,
        "y0": 0,
        "y1": 1,
        "xref": "x",
        "yref": "paper",
        "line": {"color": "red", "dash": "dash"},
        "name": "Reclassification"
    })

    for symbol in symbols_to_include:
        if symbol in data_dict and symbol in sector_names:
            data = data_dict[symbol]
            sector_name = sector_names[symbol]
            trace = go.Scatter(
                x=data.index,
                y=data["value"],
                mode="lines",
                name=sector_name  # Use the sector name as the trace name
            )
            traces.append(trace)

    figure = {
        "data": traces,
        "layout": {
            "xaxis": {"title": "Date"},
            "yaxis": {"title": "Sector Closing Price in USD"},
            "showlegend": True,
            "legend": dict(
                orientation="h",
                entrywidth=150,
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            "shapes": shapes,
            "title": title  # Set the title of the plot
        }
    }

    fig = go.Figure(figure)
    return fig   

def sector_valuation_percentage(sector_symbols, title):
    """
    Create a line plot showing the percentage of total valuation for each sector over time.

    Parameters:
    - sector_symbols: A list of sector symbols.
    - title: The title of the plot.

    Returns:
    - fig: The Plotly figure object.
    """
    # Create a list to store the traces (one for each sector)
    traces = []
    
    # Create a DataFrame to store the total valuation for each sector
    total_valuation_df = pd.DataFrame()
    
    # Find the common date range for all sectors
    common_dates = None
    for sector_symbol in sector_symbols:
        if sector_symbol in sector_stock_data_dict and sector_symbol in sector_names:
            sector_data = sector_stock_data_dict[sector_symbol]
            sector_name = sector_names[sector_symbol]
            
            if common_dates is None:
                common_dates = sector_data.index
            else:
                common_dates = common_dates.intersection(sector_data.index)
    
    # Add the sector traces and calculate total valuation
    for sector_symbol in sector_symbols:
        if sector_symbol in sector_stock_data_dict and sector_symbol in sector_names:
            sector_data = sector_stock_data_dict[sector_symbol]
            sector_name = sector_names[sector_symbol]
            
            # Create a DataFrame with the common date range
            common_data = sector_data.reindex(common_dates, fill_value=0)
            
            # Calculate total valuation for the sector
            common_data["Total Valuation"] = common_data["value"] * 1000  # Adjust scale if needed
            total_valuation_df[sector_name] = common_data["Total Valuation"]
    
    # Calculate the total valuation for all sectors at each time point
    total_valuation_df["Total"] = total_valuation_df.sum(axis=1)
    
    # Calculate the percentage of each sector"s valuation compared to the total
    for sector_symbol in sector_symbols:
        sector_name = sector_names[sector_symbol]
        percentage = (total_valuation_df[sector_name] / total_valuation_df["Total"]) * 100
        
        sector_trace = go.Scatter(
            x=common_dates,
            y=percentage,
            mode="lines",
            name=f"{sector_name} ({sector_symbol})",
        )
        traces.append(sector_trace)
    
    fig = go.Figure(traces)
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Percentage of Total Valuation",
        showlegend=True,
        legend=dict(
            orientation="h",
            entrywidth=150,
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        title=title
    )

    return fig

def heatmap_sectors(sector_stock_data_dict, sector_names, symbols_to_include):
    """
    Create a heatmap showing the pairwise correlation of sectors.

    Parameters:
    - sector_stock_data_dict: A dictionary containing sector data.
    - sector_names: A dictionary mapping sector symbols to sector names.
    - symbols_to_include: A list of sector symbols to include in the heatmap.

    Returns:
    - fig: The Plotly figure object.
    """
    # Create a DataFrame with the selected symbols
    selected_data = [sector_stock_data_dict[symbol]["value"] for symbol in symbols_to_include]
    combined_df = pd.concat(selected_data, axis=1)
    combined_df.columns = [sector_names[symbol] for symbol in symbols_to_include]

    # Calculate the correlation matrix
    df_corr = combined_df.corr()  # Generate correlation matrix

    fig = go.Figure()
    fig.update_layout(
        title="Pairwise Correlation of Sectors within S&P500 stock index"
    )
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
    """
    Update the chart based on selected sectors and plot type.

    Parameters:
    - selected_sectors: A list of sector symbols to include in the plot.
    - plot_type: The type of plot to generate ("heat", "line", "line2").

    Returns:
    - fig: The Plotly figure object.
    - text1: Text explanation for the chart (not included here).
    - text2: Text explanation for the chart (not included here).
    - text3: Text explanation for the chart (not included here).
    """
    if plot_type == "heat":
        return heatmap_sectors(sector_stock_data_dict, sector_names, selected_sectors), heatsectortext, "", ""
    elif plot_type == "line": 
        return line_plot(sector_stock_data_dict, selected_sectors, sector_names, "Sector Closing Prices over Time"), "", sectorclosetext, ""
    elif plot_type == "line2":
        return sector_valuation_percentage(selected_sectors, "Market Percentage of Sectors over Time"), "", "", ""
    else:
        return {}, "", "", ""
