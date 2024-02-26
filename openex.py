import requests
import pandas as pd
from tqdm import tqdm
import json

def load_api_id():
    with open('credentials.json', 'r') as f:
        credentials = json.load(f)
    return credentials['openexchangerates']['api_id']
        
    
def fetch_exchange_rates():
    """
    Fetches historical exchange rates from the Open Exchange Rates API and saves them in a JSON file.
    
    Returns:
    None
    """
    base_url = 'https://openexchangerates.org/api/historical/'

    headers = {"accept": "application/json"}
    params = {'app_id': load_api_id()}

    with open('data/dates.csv', 'r') as f:
        dates = pd.read_csv(f)

    dates = (dates
             .assign(review_date = pd.to_datetime(dates.review_date))
            .query('review_date >= "1999-01-01"')   
    )

    exchange_rates = {}
    for date in tqdm(dates.review_date.dt.date):
        url = base_url + str(date) + '.json'
        response = requests.get(url, headers=headers, params=params)
        exchange_rates[str(date)] = response.json()['rates']

    with open('data/exchange_rates.json', 'w') as f:
        json.dump(exchange_rates, f)
        
if __name__ == "__main__":
    fetch_exchange_rates()
    print("Exchange rates fetched and saved successfully.")
