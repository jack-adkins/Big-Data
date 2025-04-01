
try:
    import twelvedata
except ModuleNotFoundError:
    import os
    os.system("pip install twelvedata[pandas,matplotlib,plotly,websocket-client]")
    import twelvedata

import pandas as pd
import time
from datetime import datetime, timedelta
from datetime import datetime
import os
import sys
import requests

# Set your TwelveData API key
current_dir = os.path.dirname(os.path.abspath('keys.py'))
if current_dir not in sys.path:
    sys.path.append(current_dir)
from keys import twelveDataKey as api_key

# Define stock symbols and settings
symbols = ["MSFT", "AAPL"]
start_date = "2020-01-01"
end_date = "2020-12-31"
interval = 5  # seconds between "trickled" data points
init_delay_seconds = 30

#Using the Twelvedata API
def fetch_historical_data(symbol, start_date, end_date):
    url = f"https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": "1day",
        "start_date": start_date,
        "end_date": end_date,
        "apikey": API_KEY,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise error for failed requests
    data = response.json()

    if "values" in data:
        df = pd.DataFrame(data["values"])
        df["datetime"] = pd.to_datetime(df["datetime"])
        df.set_index("datetime", inplace=True)
        df = df.sort_index()
        return df["close"].astype(float)
    else:
        print(f"Error fetching data for {symbol}: {data.get('message', 'Unknown error')}", file=sys.stderr)
        return pd.Series()

# Fetch data for both stocks
print("Fetching historical data...", file=sys.stderr)
msft_prices = fetch_historical_data("MSFT", start_date, end_date)
aapl_prices = fetch_historical_data("AAPL", start_date, end_date)

if msft_prices.empty or aapl_prices.empty:
    print("Failed to fetch data. Exiting.", file=sys.stderr)
    sys.exit(1)

# Combine data into a single DataFrame
prices_df = pd.DataFrame({"MSFT": msft_prices, "AAPL": aapl_prices})
prices_df.dropna(inplace=True)  # Drop rows with missing data

# Print initialization info
print(f"Sending daily MSFT and AAPL prices from {start_date} to {end_date}...", file=sys.stderr)
print(f"... each day's data sent every {interval} seconds ...", file=sys.stderr)
print(f"... beginning in {init_delay_seconds} seconds ...", file=sys.stderr)

# Delay before starting
time.sleep(init_delay_seconds)

# Trickle-feed the data
for date, row in prices_df.iterrows():
    print(f"{date.date()}\t{row['MSFT']:.4f}\t{row['AAPL']:.4f}", flush=True)
    time.sleep(interval)
