from requests import Session
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

BASE_URL = 'https://www.coffeereview.com/review/page/'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
TOTAL_PAGES = 367
FEATURE_LIST = ['Roaster Location', 'Coffee Origin', 'Roast Level', 'Aroma', 'Acidity/Structure',
                'Acidity', 'Body','Flavor', 'Aftertaste', 'Agtron', 'Blind Assessment', 'Notes',
                'Bottom Line', 'Est. Price']

def fetch_html(session: Session, url: str) -> str:
    response = session.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print('Request failed with status code {}'.format(response.status_code))

def scrape_list_page(html:str) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('h2', class_='review-title')
    hrefs = [result.a.get('href') for result in results]
    return hrefs

def scrape_roast_page(html: str, feature_list: list) -> dict:
    
    def scrape_feature(feature):
        if soup.find('td', string=feature + ':'):
            data = (soup.find('td', string=feature + ':')
                        .find_next_sibling().text)
        elif soup.find('h2', string=feature):
            data = soup.find('h2', string=feature).find_next_sibling().text
        else:
            data = None
        return data
    
    soup = BeautifulSoup(html, 'html.parser')
    data = {feature: scrape_feature(feature) for feature in feature_list}
    return data

def main():
    urls = [BASE_URL + '{}/'.format(page_number) for page_number in range(1, TOTAL_PAGES)]
    roast_urls = []
    roast_data = []
    with Session() as session: 
        session.headers.update({'User-Agent': USER_AGENT})
        with tqdm(total=len(urls), position=0, desc='Scraping Review List: ') as pbar:
            for url in urls:
                html = fetch_html(session, url)
                hrefs = scrape_list_page(html) 
                roast_urls.extend(hrefs)
                pbar.update()
        with tqdm(total=len(roast_urls), desc='Scraping roast reviews: ') as pbar:
            for url in roast_urls:
                html = fetch_html(session, url)
                data = scrape_roast_page(html, feature_list=FEATURE_LIST)
                roast_data.append(data)
                pbar.update()
    
    df = pd.DataFrame(roast_data)
    df.to_csv('raw-roast-reviews.csv')
if __name__ == '__main__':
    main()
]