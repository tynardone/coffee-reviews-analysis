import aiohttp
import asyncio
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
from queue import Queue
import json

async def scrape_roast_page(url: str, session: aiohttp.ClientSession, results_queue: Queue):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }

    async with session.get(url, headers=headers) as response:
        response_text = await response.text()
        
    await asyncio.sleep(1) 
    soup = BeautifulSoup(response_text, 'html.parser')
    results_queue.put(soup)  # Put the soup object into the queue

async def scrape_all_roasts(urls):
    results_queue = Queue()  # Create a queue to collect soup objects
    async with aiohttp.ClientSession() as session:
        tasks = [scrape_roast_page(url, session, results_queue) for url in urls]
        await asyncio.gather(*tasks)
    return list(results_queue.queue)  # Return a list of soup objects

def scrape_feature(soup: BeautifulSoup, feature: str) -> str:
    if soup.find('td', string=feature + ':'):
        data = soup.find('td', string=feature + ':').find_next_sibling().text
    elif soup.find('h2', string=feature):
        data = soup.find('h2', string=feature).find_next_sibling().text
    else:
        data = None
    return data

if __name__ == "__main__":
    feature_list = ['Roaster Location',
                    'Coffee Origin',
                    'Roast Level',
                    'Aroma',
                    'Acidity/Structure',
                    'Acidity',
                    'Body',
                    'Flavor',
                    'Aftertaste',
                    'Agtron',
                    'Blind Assessment',
                    'Notes',
                    'Bottom Line',
                    'Est. Price']

    with open('data/raw-coffee-roasts.csv', 'r') as f:
        df_temp = pd.read_csv(f)

    urls = list(df_temp['Complete_Review_URL'])

    results = asyncio.run(scrape_all_roasts(urls))

    data = []
    for soup in results:
        data.append({feature: scrape_feature(soup, feature) for feature in feature_list})


    for i in range(len(data)):
        data[i]['url'] = urls[i]
        
    # Now, 'data' contains the scraped data for all URLs
    with open('data/async-json.json', 'w') as f:
        json.dump(data, f, indent=4)