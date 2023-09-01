from requests import Session
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

BASE_URL = 'https://www.coffeereview.com/review/page/'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
TOTAL_PAGES = 367

headers = {'User-Agent': USER_AGENT}

def fetch_list_page(session: Session, url: str, headers: dict) -> str:
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        print(response.url)
        return response.text
    else:
        print('Request failed with status code {}'.format(response.status_code))

def scrape_list_page(html) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('h2', class_='review-title')
    hrefs = [result.a.get('href') for result in results]
    return hrefs
    
def fetch_roast_page(session, url):
    return

def scrape_roast_page(session, url):
    return

def main():
    urls = [BASE_URL + '{}/'.format(page_number) for page_number in range(1, TOTAL_PAGES)]
    with Session() as session: 
        roast_urls = []
        for url in urls:
            html = fetch_list_page(session, url, headers=headers)
            urls = scrape_list_page(html) 
            roast_urls.extend(urls)
      


if __name__ == '__main__':
    main()
