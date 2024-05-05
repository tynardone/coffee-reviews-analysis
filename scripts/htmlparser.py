import logging
import re
from pathlib import Path
from bs4 import BeautifulSoup

# Function for parsing review data from HTML scraped in async_scrape_roast_reviews.py
# In main function test html is laoded from tests/html/ and parsed using function.
# FUnction needs to be able to be imported into async_scrape_roast_reviews.py

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

current_file = Path(__file__)
root_dir = current_file.parent.parent
html_dir = root_dir / 'tests' / 'html'

def _parse_tables(soup: BeautifulSoup) -> dict:
    """Extracts data from tables in the HTML.

    Args:
        soup (BeautifulSoup): BeautifulSoup object to parse

    Returns:
        dict: A dictionary containing data parsed from tables in the HTML.
    """
    data = {}
    tables = soup.find_all('table')
    for table in tables:
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) == 2:
                data[cells[0].string.strip()] = cells[1].string.strip()
    logger.info("Parsed %s table rows.", len(data))
    return data

def _parse_class(soup: BeautifulSoup, element: str, class_: str) -> str:
    """Extracts data based on element type and class.

    Args:
        soup (BeautifulSoup): BeautifulSoup object to parse
        element (str): type of html element e.g. 'p', 'h1', 'h2'
        class_ (str): class name of the element

    Returns:
        str: Data from given element and class.
    """
    found_element = soup.find(element, class_=class_)
    if found_element:
        return found_element.string.strip()
    logger.warning("No data found for %s with class %s.", found_element, class_)
    return None

def _parse_string_next(soup: BeautifulSoup, find_element: str, next_element:str, string: str, ) -> str:
    """Finds an element by type and string and returns text from the next element.
    Args:
        soup (BeautifulSoup): BeautifulSoup object to parse
        find_element (str): Element that will contain string to search for
        next_element (str): Element to extract text from
        string (str): String in the first_element 
    Returns:
        str: Data from the element after the search element containing the search string
    """
    element = soup.find(find_element, string= re.compile(string))
    if element:
        found_next_element = element.find_next(next_element)
        if found_next_element:
            return found_next_element.get_text().strip()
    return None

def _parse_notes_section(soup: BeautifulSoup) -> str:
    """Finds the notes section in the HTML and returns the text.

    Args:
        soup (BeautifulSoup): BeautifulSoup object to parse

    Returns:
        str: The text from the notes section.
    """
    notes = soup.find('h2', string=re.compile('Notes'))
    # Get text from every element after notes element until the next h2 element
    if notes:
        notes_text = ''
        for element in notes.find_next_siblings():
            if element.name == 'h2':
                break
            notes_text += element.get_text()
        return notes_text.strip()
    return None

def parse_html(html: str) -> dict: 
    """Parses HTML from coffeereview.com review html and 
    returns a dictionary of the parsed data.

    Args:
        html (str): HTML string scraped from coffeereview.com

    Returns:
        dict: A dictionary containing the parsed data.
    """
    data = {}
    soup = BeautifulSoup(html, 'html.parser')

    rating = _parse_class(soup, 'span', 'review-template-rating')
    roaster = _parse_class(soup, 'p', 'review-roaster')
    title = _parse_class(soup, 'h1', 'review-title')

    blind_assessment = _parse_string_next(soup, 'h2', 'p', 'Blind Assessment')
    # TODO: Some notes have a p and a span tag, with the span carrying just links so need to pull both
    # see https://www.coffeereview.com/review/panama-geisha-aroma-roast/ for an example
    # Some have n <i> tag see https://www.coffeereview.com/review/camilina-geisha/. 
    # Looks like will have to pull all text from all elements between Notes and Bottom Line
    
    notes = _parse_notes_section(soup)

    # Older reviews do NOT have a bottom line
    bottom_line = _parse_string_next(soup, 'h2', 'p', 'Bottom Line')

    table_data = _parse_tables(soup)

    data['rating'] = rating
    data['roaster'] = roaster
    data['title'] = title
    data['blind assessment'] = blind_assessment
    data['notes'] = notes
    data['bottom line'] = bottom_line
    data.update(table_data)

    n_fields = len(data)
    logging.info("Parsed %s data fields for %s - %s.", n_fields, roaster, title)
    return data

if __name__ == '__main__':
    html_files = list(html_dir.glob('*.html'))
    for file in html_files:
        with open(file, 'r', encoding='utf-8') as f:
            html = f.read()
            data = parse_html(html)
            print(data)
