import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

# TODO: These Functions are doing tooo much!!!!
def scrape_roast_list(session: requests.Session) -> list[dict]:

    def scrape_page(page_number: int) -> list[dict]:
        page_data = []
        headers = {'user-agent':
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
                   'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                   '113.0.0.0 Safari/537.36'}
        url = ('https://www.coffeereview.com/advanced-search/page/{}/'
               .format(page_number))
        # Send a GET request to the URL
        response = session.get(url, headers=headers)

        # Create a BeautifulSoup object
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the relevant HTML elements and extract the desired data
        main = soup.find('main')
        results = main.find_all('div', class_='entry-content')

        # Loop through list of entries and extract data
        for result in results:
            rating = result.find('span', class_='review-template-rating').text

            # Extract the coffee roaster name
            roaster = result.find('p', class_='review-roaster').a.text

            # Extract the coffee name
            name = result.find('h2', class_='review-title').a.text

            # Extract the review date
            review_date = (result.find('div', class_='column col-3')
                           .strong.next_sibling.strip())

            # Extract the review description
            description = result.find('div', class_='row row-2').p.string

            # Extract the URL for complete review   - TODO
            row_3 = result.find('div', class_='row row-3').find_all('div')
            try:
                roast_url = row_3[0].a['href']
            except:
                roast_url = None

            # Extract the URL for the roaster's website
            try:
                roaster_website_url = row_3[1].a['href']
            except:
                roaster_website_url = None

            row_data = {
                'Rating': rating,
                'Roaster': roaster,
                'Coffee_Name': name,
                'Review_Date': review_date,
                'Review_Description': description,
                'Complete_Review_URL': roast_url,
                'Roaster_Website_URL': roaster_website_url
                }

            page_data.append(row_data)

        return page_data

    # Initialize list to hold all data
    data = []

    # Loop through all pages and scrape data
    for i in tqdm(range(0, 121), position=0, leave=True, desc="Scraping Review List: "):
        page_data = scrape_page(i)
        data.extend(page_data)
    return data


def scrape_roast_page(url: str, session: requests.Session) -> dict:
    """Scrape the data from a single review page.

    Args:
        url (str): The URL of the review page.
        session (requests.Session): The session object to use for the request.

    Returns:
        dict: The scraped roast data.
    """

    # This header is required
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
               'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0'
               'Safari/537.36'}
    response = session.get(url=url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    def scrape_feature(feature):
        if soup.find('td', string=feature + ':'):
            data = (soup.find('td', string=feature + ':')
                        .find_next_sibling().text)
        elif soup.find('h2', string=feature):
            data = soup.find('h2', string=feature).find_next_sibling().text
        else:
            data = None
        return data

    feature_list = ['Roaster Location',
                    'Coffee Origin',
                    'Roast Level',
                    'Aroma',
                    'Acidity/Structure',
                    'Acidity',
                    'Body',
                    'Flavor',
                    'Aftertaste',
                    'Agtron',
                    'Blind Assessment',
                    'Notes',
                    'Bottom Line',
                    'Est. Price']

    data = {feature: scrape_feature(feature) for feature in feature_list}
    data['url'] = url
    return data

def main():
    pass
if __name__ == "__main__":
    with requests.Session() as session:
        data = scrape_roast_list(session=session)

        df1 = pd.DataFrame(data)
        urls = list(df1['Complete_Review_URL'])

        
        roast_data = []

        with tqdm(total=len(urls), position=0, leave=True, desc="Scraping Roast Data: ") as pbar:
            for url in urls:
                roast = scrape_roast_page(url, session)
                roast_data.append(roast)
                pbar.update()

    df2 = pd.DataFrame(roast_data)
    df = df1.merge(df2, left_on="Complete_Review_URL", right_on="url")
    df.to_csv('data/raw-roast-reviews.csv', index=False)