import json
import requests
import pandas as pd
from dotenv import load_dotenv
from rich.progress import Progress

def load_api_id():
    """Loads the Open Exchange Rates API ID from a JSON file."""
    with open('config/credentials.json', 'r', encoding='utf-8') as f:
        credentials = json.load(f)
    return credentials['openexchangerates']['api_id']

def fetch_rate_for_date(date, headers, params):
    """Fetches exchange rates for a specific date."""
    base_url = 'https://openexchangerates.org/api/historical/'
    url = f"{base_url}{date}.json"
    response = requests.get(url, headers=headers, params=params, timeout=10)
    return response.json()['rates']

def fetch_exchange_rates():
    """Fetches historical exchange rates and saves them in a JSON file."""
    headers = {"accept": "application/json"}
    params = {'app_id': load_api_id()}
    exchange_rates = {}

    dates = pd.read_csv('data/dates.csv')
    dates = (dates.assign(review_date=pd.to_datetime(dates.review_date))
             .query('review_date >= "1999-01-01"'))

    with Progress() as progress:
        task = progress.add_task("[green]Fetching exchange rates...", total=len(dates))
        for date in dates.review_date.dt.date:
            exchange_rates[str(date)] = fetch_rate_for_date(date, headers, params)
            progress.update(task, advance=1)
    return exchange_rates

def main():
    """Fetch historical exchange rates and save them to a JSON file."""
    exchange_rates = fetch_exchange_rates()
    with open('data/external/exchange_rates.json', 'w', encoding='utf-8') as f:
        json.dump(exchange_rates, f)
    print("Exchange rates fetched and saved successfully.")

if __name__ == "__main__":
    main()
