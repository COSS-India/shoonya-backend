from typing import Optional

import requests
from bs4 import BeautifulSoup


def scrape_links(url: str) -> Optional[list[str]]:
    """
    Scrapes a webpage for 'a' tags with rel='bookmark' inside a specific div.
    Args:
        url (str): The URL of the webpage to scrape.
    """
    try:
        # We send a GET request to the URL. We use a timeout to prevent hanging.
        response = requests.get(url, timeout=10)
        # Raise an exception if the request was unsuccessful (e.g., 404, 500)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

    # Parse the HTML content using 'html.parser'.
    # For more robust parsing, you could install and use 'lxml'.
    soup = BeautifulSoup(response.content, 'html.parser')

    # We locate the div element with the specific id 'this_id'
    target_div = soup.find('div', id='tdi_93')

    if target_div:
        bookmark_links = target_div.select('#tdi_93 div.td-module-meta-info > h3 > a')

        if not bookmark_links:
            print("No <a> tags with rel='bookmark' found inside the target div.")
            return None

        print(f"Found {len(bookmark_links)} bookmark links:")
        links = []
        for link in bookmark_links:
            # Extract the href attribute (the URL) and the text of the link
            href = link.get('href', 'No URL found')
            text = link.text.strip()
            print(f"- Text: {text} | URL: {href}")
            links.append(href)
        return links

    else:
        print("Could not find the div with id='this_id' on the page.")
        return None