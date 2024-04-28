import logging
from bs4 import BeautifulSoup
from rich import print

# Setup basic configuration for logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_tables(soup: BeautifulSoup) -> dict:
    """
    Parse tables from the HTML content and return a dictionary of key-value pairs.
    """
    table_data = {}
    tables = soup.find_all('table')
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:  # Ensure there are at least two columns
                key = cols[0].text.strip()
                value = cols[1].text.strip()
                table_data[key] = value
    return table_data

def safe_find_text(soup, selector, attribute=None, find_next_selector=None, **kwargs):
    """ 
    Find text in a BeautifulSoup object and return it.
    """
    try:
        element = soup.find(selector, **kwargs)
        if attribute:
            return getattr(element, attribute)().text.strip()
        if find_next_selector:
            return element.find_next(find_next_selector).text.strip()
        return element.text.strip()

    except AttributeError as e:
        logging.error(
           "Failed to find text for %s with attributes %s or error in %s: %s",
           selector, kwargs, find_next_selector, e
           )
        return None

def parse_html(html: str) -> dict:
    """ 
    Parse HTML content and return a dictionary of key-value pairs.
    """
    soup = BeautifulSoup(html, 'lxml')
    data = {
        'rating': safe_find_text(soup, 'div', class_='review-template-rating'),
        'roaster': safe_find_text(soup, 'div', class_='review-roaster'),
        'name': safe_find_text(soup, 'h1', class_='review-title'),
        'blind_assessment': safe_find_text(soup, 'h2', text='Blind Assessment',
                                           find_next_selector='p'
                                           ),
        'notes': safe_find_text(soup, 'h2', text='Notes', find_next_selector='p'),
        'bottom_line': safe_find_text(soup, 'h2', text='Bottom Line', find_next_selector='p')
    }
    data.update(parse_tables(soup))
    return data

if __name__ == '__main__':
    with open('dev/main2.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    parsed_data = parse_html(html_content)
    print(parsed_data)
