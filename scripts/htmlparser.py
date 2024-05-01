import logging
import re
from pathlib import Path
from bs4 import BeautifulSoup

# Function for parsing review data from HTML scraped in async_scrape_roast_reviews.py
# In main function test html is laoded from tests/html/ and parsed using function.
# FUnction needs to be able to be imported into async_scrape_roast_reviews.py

current_file = Path(__file__)
root_dir = current_file.parent.parent
html_dir = root_dir / 'tests' / 'html'

def _parse_tables(soup: BeautifulSoup) -> dict:
    """Extracts data from all tables."""
    data = {}
    tables = soup.find_all('table')
    for table in tables:
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) == 2:
                data[cells[0].string.strip()] = cells[1].string.strip()
    return data

def _parse_class(soup: BeautifulSoup, element: str, class_: str) -> str:
    """Extracts data from a specific class."""
    try:
        return soup.find(element, class_=class_).string.strip()
    except AttributeError:
        return None

def _parse_string_next(soup: BeautifulSoup, find_element: str, next_element:str, string: str, ) -> str:
    """Extracts data from a specific string."""
    try:
        return (soup
                .find(find_element, string= re.compile(string))
                .find_next(next_element)
                .get_text().strip()
        )
    except AttributeError:
        return None

def parse_html(html: str) -> dict:
    """ Parse HTML content and return a dictionary of key-value pairs."""
    data = {}
    soup = BeautifulSoup(html, 'html.parser')

    rating = _parse_class(soup, 'p', 'review-rating')
    roaster = _parse_class(soup, 'p', 'review-roaster')
    title = _parse_class(soup, 'h1', 'review-title')

    blind_assessment = _parse_string_next(soup, 'h2', 'p', 'Blind Assessment')
    notes = _parse_string_next(soup, 'h2', 'span', 'Notes')
    bottom_line = _parse_string_next(soup, 'h2', 'p', 'Bottom Line')

    table_data = _parse_tables(soup)

    data['rating'] = rating
    data['roaster'] = roaster
    data['title'] = title
    data['blind assessment'] = blind_assessment
    data['notes'] = notes
    data['bottom line'] = bottom_line
    data.update(table_data)
    
    return data


if __name__ == '__main__':
    html_files = [file for file in html_dir.glob('*.html')]
    for file in html_files:
        with open(file, 'r', encoding='utf-8') as f:
            html = f.read()
            data = parse_html(html)
            print(data)
            
