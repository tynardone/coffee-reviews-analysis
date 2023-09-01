from requests import Session
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

BASE_URL = 'https://www.coffeereview.com/review/page/'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
TOTAL_PAGES = 367

headers = {'User-Agent': USER_AGENT}

def fetch_list_page(session: Session, page_number: int, headers: dict) -> str:
    url = BASE_URL + '{}/'.format(page_number)
    print(url)
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        print(response.url)
        return response.text
    else:
        print('Request failed with status code {}'.format(response.status_code))

def scrape_list_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('h2', class_='review-title')
    for result in results:
        out = [result.a.get('href') for result in results]
    return out
    
def fetch_roast_page(session, url):
    return

def scrape_roast_page(session, url):
    return

def main():
    with Session() as session: 
        html = fetch_list_page(session, 2, headers=headers)
        out = scrape_list_page(html)
        print(out)
      


if __name__ == '__main__':
    main()
