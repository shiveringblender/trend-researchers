import os
import pandas as pd


window_size = 52
stock_data_dict = {}
avg_price_before_event_dict = {}
avg_price_after_event_dict = {}
std_dev_before_event_dict = {}
std_dev_after_event_dict = {}
csv_folder = 'csv_data_events_weekly_adjusted'
csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]
for csv_file in csv_files:
    # Extract the symbol from the CSV filename 
    symbol = os.path.splitext(csv_file)[0].split('_')[0]

    # Load the CSV data into a DataFrame
    data = pd.read_csv(os.path.join(csv_folder, csv_file), index_col=0, parse_dates=True)

    # Store the data in stock_data_dict with the symbol as the key
    stock_data_dict[symbol] = data

