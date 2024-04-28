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
from review_parse import parse_html

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36\
             (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'

FEATURE_LIST = ['Roaster Location', 'Coffee Origin', 'Roast Level', 'Aroma',
                'Acidity/Structure', 'Acidity', 'Body', 'Flavor', 'Aftertaste',
                'Agtron', 'Blind Assessment', 'Notes', 'Bottom Line',
                'Est. Price']


async def scrape_roast_review(session: AsyncHTMLSession, url: str, progress: tqdm) -> dict:

    r = await session.get(url)
    if r.status_code in (429, 504):
        await asyncio.sleep(3)  # Adjust the delay time (in seconds) as needed
        return await scrape_roast_review(session, url, progress)
    data = parse_html(r.text)
    data['url'] = url
    progress.update()
    return data


async def main(urls: list[str], progress: tqdm):
    session = AsyncHTMLSession()
    tasks = [scrape_roast_review(session, url, progress) for url in urls]
    return await asyncio.gather(*tasks)

if __name__ == '__main__':
    with open('data/roast-urls.pkl', 'rb') as f:
        urls = pickle.load(f)

    start = perf_counter()
    progress_bar = tqdm(total=len(urls), desc="Scraping roast pages")
    results = asyncio.run(main(urls, progress=progress_bar))
    progress_bar.close()
    end = perf_counter()

    print(results)
    print(f"Ran in {end- start:0.4f} seconds")

    with open('data/raw-roast-reviews.json', 'w', encoding="utf-8") as fout:
        json.dump(results, fout)
