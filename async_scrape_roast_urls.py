"""
ROAST REVIEW URL SCRAPER

This script scrapes the URLs for all individual roast reviews from the review list pages
on coffeereview.com. The URLs are pickled and saved to data/roast-urls.pkl
to be used by async_scrape_roast_reviews.py.
"""
from requests_html import AsyncHTMLSession
from tqdm import tqdm
import asyncio
import aiohttp
import pickle

BASE_URL = 'https://www.coffeereview.com/review/page/'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
TOTAL_PAGES = 379

async def scrape_review_list(session: AsyncHTMLSession, url: str, pbar:tqdm) -> list[str]:
    """
    Scrapes urls for all individual roast reviews from a single review list page.

    Args:
        session (AsyncHTMLSession): The async HTML session to use for the request.
        url (str): The URL of the review list page to scrape.
        pbar (tqdm): The progress bar to update.

    Returns:
        list[str]: A list of URLs for all individual roast reviews found on the page.
    """
    r = await session.get(url)
    links = r.html.links
    links = [l for l in links if '/review/' in l and '/page/' not in l]
    if r.status_code == 429 or r.status_code == 504:
        await asyncio.sleep(3)  # You can adjust the delay time (in seconds) as needed
        return await scrape_review_list(session, url, pbar)
    else:
        pbar.update()
        return links
    
async def main(urls: list[str], pbar: tqdm):
    session = AsyncHTMLSession()
    tasks = [scrape_review_list(session, url, pbar) for url in urls]
    return await asyncio.gather(*tasks)
           
if __name__ == '__main__':
   links = []
   # List of all urls for the roast review list pages
   urls = [BASE_URL + '{}/'.format(page_number) for page_number in range(1, TOTAL_PAGES)]
   pbar = tqdm(total=len(urls), desc="Scraping roast urls")
   # Results is a list of lists
   results = asyncio.run(main(urls, pbar))
   pbar.close()
   flat_list = [item for sublist in results for item in sublist]
   print("Found {} URLS".format(len(flat_list)))
   
   with open('data/roast-urls.pkl', 'wb') as fout: 
       pickle.dump(flat_list, fout)
       
   
   
       