import os
import pandas as pd


window_size = 52
weeklyadj_stock_data_dict = {}
weeklyadj_csv_folder = 'csv_data_events_weekly_adjusted'
weeklyadj_csv_files = [f for f in os.listdir(weeklyadj_csv_folder) if f.endswith('.csv')]
for weeklyadj_csv_file in weeklyadj_csv_files:
    # Extract the symbol from the CSV filename 
    symbol = os.path.splitext(weeklyadj_csv_file)[0].split('_')[0]

    # Load the CSV data into a DataFrame
    data = pd.read_csv(os.path.join(weeklyadj_csv_folder, weeklyadj_csv_file), index_col=0, parse_dates=True)

    # Store the data in stock_data_dict with the symbol as the key
    weeklyadj_stock_data_dict[symbol] = data

sector_stock_data_dict = {}
sector_csv_folder = 'sector_data'
sector_csv_files = [f for f in os.listdir(sector_csv_folder) if f.endswith('.csv')]
for sector_csv_file in sector_csv_files:
    # Extract the symbol from the CSV filename 
    symbol = os.path.splitext(sector_csv_file)[0].split('_')[0]

    # Load the CSV data into a DataFrame
    data = pd.read_csv(os.path.join(sector_csv_folder, sector_csv_file), index_col=0, parse_dates=True)

    # Store the data in stock_data_dict with the symbol as the key
    sector_stock_data_dict[symbol] = data
    
# Dictionary of sector symbols and names
sector_names = {
    "XLC":  "Communication Services",
    "XLY":  "Consumer Discretionary",
    "XLP":  "Consumer Staples",
    "XLE":  "Energy",
    "XLF":  "Financials",
    "XLV":  "Health Care",
    "XLI":  "Industrials",
    "XLB":  "Materials",
    "XLRE": "Real Estate",
    "XLK":  "Technology",
    "XLU":  "Utilities",
}
smp_data_dict = {}
smp_csv_folder = 'us'
smp_csv_files = [f for f in os.listdir(smp_csv_folder) if f.endswith('.csv')]
for smp_csv_file in smp_csv_files:
    # Extract the symbol from the CSV filename 
    symbol = os.path.splitext(smp_csv_file)[0].split('_')[0]

    # Load the CSV data into a DataFrame
    data = pd.read_csv(os.path.join(smp_csv_folder, smp_csv_file), index_col=0, parse_dates=True)

    # Store the data in stock_data_dict with the symbol as the key
    smp_data_dict[symbol] = data
nasdaq_stock_name_dict = {}
nasdaq_path= 'nasdaq/nasdaq.csv'
nasdaqdf = pd.read_csv(nasdaq_path)
nasdaq_dict = nasdaqdf.to_dict(orient='records')
nasdaq_dict = nasdaqdf.set_index('Symbol')['Company Name'].to_dict()
sentiment_data = 'sentiment_data/sentiment.csv'
sentimentdf = pd.read_csv(sentiment_data)
sentimentdf["Date"] = pd.to_datetime(sentimentdf["Date"])
us_data = {
    'GDP' : {'name':"US Gross domestic product", 'title': 'US Gross domestic product', 'unit': 'billions of US-Dollars'},
    'SPY' : {'name':"S&P500 stock index", 'title': 'S&P500 stock index monthly adjusted closing prices', 'unit': 'Closing price in US-Dollars'},
    'UEM' : {'name: "US Unemploymentrate", title': 'US Unemploymentrate', 'unit': 'percent'},
    'INF' : {'name':"US Inflation", 'title': 'US Inflation', 'unit': 'percent'}
}

