import logging
from pathlib import Path
from bs4 import BeautifulSoup
from rich import print

# Setup basic configuration for logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

base_path = Path(__file__).parent.parent
test_html_path = base_path / 'tests/test_review_parse.html'

def parse_table_soup(soup: BeautifulSoup) -> dict:
    """Parse tables from the HTML content and return a dictionary of key-value pairs."""
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

def find_text(soup, selector, attribute=None, find_next_selector=None, **kwargs):
    """ Find text in a BeautifulSoup object and return it."""
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

def parse_review_soup(soup: BeautifulSoup) -> dict:
    """ Parse HTML content and return a dictionary of key-value pairs."""
    data = {
        'rating': find_text(soup, 'div', class_='review-template-rating'),
        'roaster': find_text(soup, 'div', class_='review-roaster'),
        'name': find_text(soup, 'h1', class_='review-title'),
        'blind_assessment': find_text(soup, 'h2', text='Blind Assessment',
                                           find_next_selector='p'
                                           ),
        'notes': find_text(soup, 'h2', text='Notes', find_next_selector='p'),
        'bottom_line': find_text(soup, 'h2', text='Bottom Line', find_next_selector='p')
    }
    data.update(parse_tables(soup))
    return data

def main() -> None:
    with open(test_html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    parsed_data = parse_review_soup(soup)
    print(parsed_data)

if __name__ == '__main__':
    main()
