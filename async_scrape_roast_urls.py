from requests_html import AsyncHTMLSession
import asyncio
import pickle

BASE_URL = 'https://www.coffeereview.com/review/page/'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
FEATURE_LIST = ['Roaster Location', 'Coffee Origin', 'Roast Level', 'Aroma', 'Acidity/Structure',
                'Acidity', 'Body','Flavor', 'Aftertaste', 'Agtron', 'Blind Assessment', 'Notes',
                'Bottom Line', 'Est. Price']
TOTAL_PAGES = 367

# Function to retrieve and pars out review urls
async def scrape_review_list(session: AsyncHTMLSession, url: str):
    r = await session.get(url)
    links = r.html.links
    links = [l for l in links if '/review/' in l and '/page/' not in l]
    if r.status_code == 429 or r.status_code == 504:
        await asyncio.sleep(3)  # You can adjust the delay time (in seconds) as needed
        return await scrape_review_list(session, url)
    else:
        return links
    
async def main(urls):
    session = AsyncHTMLSession()
    tasks = [scrape_review_list(session, url) for url in urls]
    return await asyncio.gather(*tasks)
           
if __name__ == '__main__':
   links = []
   urls = [BASE_URL + '{}/'.format(page_number) for page_number in range(1, TOTAL_PAGES)]
   results = asyncio.run(main(urls))
   flat_list = [item for sublist in results for item in sublist]
   print("Found {} URLS".format(len(flat_list)))
   
   with open('data/roast-urls.pkl', 'wb') as fout: 
       pickle.dump(flat_list, fout)
       
   
   
       