import asyncio
from requests_html import AsyncHTMLSession
from tqdm import tqdm
from bs4 import BeautifulSoup
from time import perf_counter
import pandas as pd 
import pickle

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
FEATURE_LIST = ['Roaster Location', 'Coffee Origin', 'Roast Level', 'Aroma', 'Acidity/Structure',
                'Acidity', 'Body','Flavor', 'Aftertaste', 'Agtron', 'Blind Assessment', 'Notes',
                'Bottom Line', 'Est. Price']

def scrape_feature(feature: str, soup: BeautifulSoup) -> str:
    if soup.find('td', string=feature + ':'):
        data = (soup.find('td', string=feature + ':')
                    .find_next_sibling().text)
    elif soup.find('h2', string=feature):
        data = soup.find('h2', string=feature).find_next_sibling().text
    else:
        data = None
    return data

async def fetch_url(session: AsyncHTMLSession, url: str) -> str:
    r = await session.get(url)
    if r.status_code == 429 or r.status_code == 504:
        await asyncio.sleep(3)  # You can adjust the delay time (in seconds) as needed
        return await fetch_url(session, url)
    else:
        pbar.update()
        return r.text

async def process_html(html: str, pbar: tqdm, url) -> dict:
    soup = BeautifulSoup(html, 'html.parser')
    roast_review = {feature: scrape_feature(feature, soup) for feature in FEATURE_LIST}
    roast_review['url'] = url
    return roast_review

async def main(urls: list[str], pbar: tqdm):
    session = AsyncHTMLSession()
    tasks = [fetch_url(session, url) for url in urls]
    html_responses = await asyncio.gather(*tasks)
    
    results = []
    for html, url in zip(html_responses, urls):
        results.append(await process_html(html, pbar=pbar, url=url))
    
    return results

# ...

if __name__ == '__main__':
    
    with open('data/roast-urls.pkl', 'rb') as f:
        urls = pickle.load(f)
        
    start = perf_counter()
    pbar = tqdm(total=len(urls), desc="Scraping roast pages")
    results = asyncio.run(main(urls, pbar))
    pbar.close()
    end = perf_counter()

    print(len(results))
    print(f"Ran in {end- start:0.4f} seconds")

    df = pd.DataFrame(results)
    df.to_csv('data/raw_roast_reviews.csv', index=False)
