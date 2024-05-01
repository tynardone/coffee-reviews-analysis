import logging
from dataclasses import dataclass
from pathlib import Path
from bs4 import BeautifulSoup

# Function for parsing review data from HTML scraped in async_scrape_roast_reviews.py
# In main function test html is laoded from tests/html/ and parsed using function.
# FUnction needs to be able to be imported into async_scrape_roast_reviews.py

current_file = Path(__file__)
root_dir = current_file.parent.parent
html_dir = root_dir / 'tests' / 'html'

def parse_html(html: str) -> dict:
    """ Parse HTML content and return a dictionary of key-value pairs."""
    data = {}
    soup = BeautifulSoup(html, 'html.parser')
    # rating
    # roaster
    # title
    # roaster location
    # coffee origin
    # roast level
    # agtron
    # est price
    # review date
    # aroma
    # acidit/sructure
    # acidity
    # body
    # flavor
    # aftertaste
    # blind assessment
    # notes
    # bottom line
    
    return data

if __name__ == '__main__':
    html_files = [file for file in html_dir.glob('*.html')]