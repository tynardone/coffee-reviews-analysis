from bs4 import BeautifulSoup
from rich import print

def scrape_data(soup:BeautifulSoup) -> dict:
    # Takes one BeautifulSoup object of a roast review page and returns a dict
    # of scraped data. 
    data = {}
    
    def parse_tables(soup: BeautifulSoup):
        table_data = {}
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                key = cols[0].text
                if cols[1]:
                    value = cols[1].text
                else:
                    value =None
                table_data[key] = value
        return table_data
    
    def extract_or_none(soup, class_:str) -> str:
        if soup.find(class_=class_).text:
            return soup.find(class_=class_).text
        else:
            return None

    data.update(parse_tables(soup))
    data['rating'] = extract_or_none(soup, class_='review-template-rating')
    data['roaster'] = extract_or_none(soup, class_='review-roaster')
    data['name'] = extract_or_none(soup, class_='review-title')

    return data

if __name__ == '__main__':
    with open('main.html', 'r') as f:
        main = f.read()
    soup = BeautifulSoup(main, 'lxml')
    print(scrape_data(soup=soup))