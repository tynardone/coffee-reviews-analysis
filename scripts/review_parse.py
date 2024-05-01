import logging
from pathlib import Path
from bs4 import BeautifulSoup
from rich import print

# Setup basic configuration for logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Set project directory root and path to html file for testing 
base_path = Path(__file__).parent.parent
test_html_path = base_path / 'tests/test_review_parse.html'

def parse_tables_soup(soup: BeautifulSoup) -> dict:
    """Parse tables from the HTML content and return a dictionary of key-value pairs."""
    table_data = {}
    tables = soup.find_all('table')
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:  # Ensure there are at least two columns
                key = cols[0].string.strip()
                value = cols[1].string.strip()
                table_data[key] = value
    return table_data

def find_string(soup, selector, attribute=None, find_next_selector=None, **kwargs):
    """ Find string in a BeautifulSoup object and return it."""
    try:
        element = soup.find(selector, **kwargs)
        if attribute:
            return getattr(element, attribute)().string.strip()
        if find_next_selector:
            next_element= element.find_next(find_next_selector)
            if next_element:
                return next_element.get_text().strip()
        return element.string.strip()

    except AttributeError as e:
        logging.error(
           "Failed to find string for %s with attributes %s or error in %s: %s",
           selector, kwargs, find_next_selector, e
           )
        return None

def parse_review_soup(html: str) -> dict:
    """ Parse HTML content and return a dictionary of key-value pairs."""
    soup = BeautifulSoup(html, 'html.parser')
    data = {
        'rating': find_string(soup, 'span', class_='review-template-rating'),
        'roaster': find_string(soup, 'p', class_='review-roaster'),
        'name': find_string(soup, 'h1', class_='review-title'),
        'blind_assessment': find_string(soup, 'h2', string='Blind Assessment',
                                           find_next_selector='p'
                                           ),
        'notes': find_string(soup, 'h2', string='Notes', find_next_selector='p'),
        'bottom_line': find_string(soup, 'h2', string='Bottom Line', find_next_selector='p')
    }
    data.update(parse_tables_soup(soup))
    return data

def main() -> None:
    """Main function to test the parsing functions.
    """
    with open(test_html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    parsed_data = parse_review_soup(html_content)
    print(parsed_data)

if __name__ == '__main__':
    main()
