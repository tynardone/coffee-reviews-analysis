from requests_html import AsyncHTMLSession
from tqdm import tqdm
import asyncio
import pickle
from dataclasses import dataclass

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
FEATURE_LIST = ['Roaster Location', 'Coffee Origin', 'Roast Level', 'Aroma', 'Acidity/Structure',
                'Acidity', 'Body','Flavor', 'Aftertaste', 'Agtron', 'Blind Assessment', 'Notes',
                'Bottom Line', 'Est. Price']

@dataclass
class RoastReview:
    roaster_location: str
    coffee_origin: str
    roast_level: str
    aroma: int
    acidity: int
    body: int
    flavor: int
    aftertaste: int
    agtron: str
    blind_assessment: str
    notes: str
    bottom_line: str
    price: str
    
    
async def scrape_roast_review(session: AsyncHTMLSession, url: str, pbar:tqdm) -> RoastReview:
    r = await session.get(url)
    # Process r
    if r.status_code == 429 or r.status_code == 504:
        await asyncio.sleep(3)  # You can adjust the delay time (in seconds) as needed
        return await scrape_roast_review(session, url, pbar)
    else:
        pbar.update()
        return RoastReview
    
async def main(urls: list[str], pbar: tqdm):
    session = AsyncHTMLSession()
    tasks = [scrape_roast_review(session, url, pbar) for url in urls]
    return await asyncio.gather(*tasks)
           
if __name__ == '__main__':
    with open('data/roast-urls.pkl', 'rb') as f:
        urls = pickle.load(f)
        
    pbar = tqdm(total=len(urls), desc="Scraping roast urls")
    results = asyncio.run(main(urls, pbar))
    pbar.close()
    
    
       
   
   
       