from bs4 import BeautifulSoup
from rich import print

def parse_html(html: str) -> dict:
    # Takes one BeautifulSoup object of a roast review page and returns a dict
    # of scraped data. 
    soup = BeautifulSoup(html, 'lxml')
    data = {}
    
    def parse_tables(soup: BeautifulSoup):
        table_data = {}
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                key = cols[0].text
                value = cols[1].text
                table_data[key] = value
        return table_data
    
    def extract_class(soup, class_:str) -> str:
        try:
            return soup.find(class_=class_).text
        except:
            return None

    data.update(parse_tables(soup))
    data['rating'] = extract_class(soup, class_='review-template-rating')
    data['roaster'] = extract_class(soup, class_='review-roaster')
    data['name'] = extract_class(soup, class_='review-title')

    return data

if __name__ == '__main__':
    with open('dev/main2.html', 'r') as f:
        main = f.read()
        print(main)
    print(parse_html(main))