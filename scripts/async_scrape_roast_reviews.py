"""
ASYNC ROAST REVIEW SCRAPER

This script loads a list of roast review URLs from data/roast-urls.pkl and scrapes the
review data from each page. The data is saved to data/raw-roast-reviews.json
for further processing.
"""
import asyncio
import pickle
import json
from time import perf_counter

from requests_html import AsyncHTMLSession
from tqdm import tqdm
from bs4 import BeautifulSoup
from review_parse import parse_review_soup

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36\
             (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
FEATURE_LIST = ['Roaster Location', 'Coffee Origin', 'Roast Level', 'Aroma',
                'Acidity/Structure', 'Acidity', 'Body', 'Flavor', 'Aftertaste',
                'Agtron', 'Blind Assessment', 'Notes', 'Bottom Line',
                'Est. Price']
DATA_INPUT = 'data/raw/roast-urls.pkl'
DATA_OUTPUT = 'data/raw/raw-roasts-reviews-test.json'

async def scrape_roast_review(session: AsyncHTMLSession, url: str, progress: tqdm) -> dict:
    r = await session.get(url)
    if r.status_code in (429, 504):
        await asyncio.sleep(3)  # Adjust the delay time (in seconds) as needed
        return await scrape_roast_review(session, url, progress)
    soup = BeautifulSoup(r.text, 'html.parser')
    div_content = soup.find('div', class_='entry-content')
    progress.update(1)
    return {"url": url, "html": div_content.prettify()}

async def gather_tasks(urls: list[str], progress: tqdm):
    session = AsyncHTMLSession()
    tasks = [scrape_roast_review(session, url, progress) for url in urls]
    return await asyncio.gather(*tasks)

def main():
    with open(DATA_INPUT, 'rb') as f:
        urls = pickle.load(f)

    start = perf_counter()
    progress_bar = tqdm(total=len(urls), desc="Scraping roast pages")
    results = asyncio.run(gather_tasks(urls, progress=progress_bar))
    progress_bar.close()
    end = perf_counter()

    print(f"Ran in {end- start:0.4f} seconds")

    with open('output.json', 'w', encoding='utf-8') as fout:
        json.dump(results, fout)

    with open('output.json', 'r', encoding='utf-8') as fin:
        data = json.load(fin)
        soup = BeautifulSoup(data[0]['html'], 'html.parser')
        print(soup.prettify())
        
if __name__ == '__main__':
    main()