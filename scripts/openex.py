import json
import os
import requests
import pandas as pd
from dotenv import load_dotenv
from rich.progress import Progress

# Load environment variables from .env file
load_dotenv()

# Constants
DATES_CSV_PATH = '../data/interim/dates.csv'
OUTPUT_JSON_PATH = '../data/external/openex_exchange_rates.json'
BASE_URL = 'https://openexchangerates.org/api/historical/'

def load_api_id() -> str:
    """Loads the OpenExchangeRates API ID from the environment.

    Returns:
        str: OpenExchangeRates API ID
    """
    return os.getenv('OPENEXCHANGERATES_API_ID')

def load_date_list(file_path: str) -> list[str]:
    """Loads a list of dates from a CSV file.

    Args:
        file_path (str): Path to the CSV file containing dates

    Returns:
        list[str]: List of dates
    """
    dates = pd.read_csv(file_path)
    dates = (dates.assign(review_date=pd.to_datetime(dates.review_date))
             .query('review_date >= "1999-01-01"'))
    return dates.review_date.dt.date.tolist()

def fetch_rate_for_date(date: str, base_url: str, headers: dict,
                        params: dict) -> dict[str, list[float]]:
    """Fetches historical exchange rates for a given date.

    Args:
        date (str): YYYY-MM-DD formatted date string
        base_url (str): Base URL for the API
        headers (dict): Request headers
        params (dict): Request parameters

    Returns:
        dict[str, list[float]]: List of exchange rates for the given date
    """
    url = f"{base_url}{date}.json"
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    return response.json()['rates']

def main():
    """Fetch and save exchange rates for provided dates."""
    headers = {"accept": "application/json"}
    params = {'app_id': load_api_id()}

    dates = load_date_list(DATES_CSV_PATH)
    exchange_rates = {}

    with Progress() as progress:
        task = progress.add_task("[green]Fetching exchange rates...", total=len(dates))                        
        for date in dates:
            exchange_rates[str(date)] = fetch_rate_for_date(date,
                                                            base_url=BASE_URL,
                                                            headers=headers,
                                                            params=params)
            progress.advance(task)

    with open(OUTPUT_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(exchange_rates, f)
    print("Exchange rates fetched and saved successfully.")

if __name__ == "__main__":
    main()
