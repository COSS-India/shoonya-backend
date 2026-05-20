import asyncio
from typing import Optional

import httpx
from bs4 import BeautifulSoup


async def scrape_links(url: str, client: httpx.AsyncClient) -> Optional[list[str]]:
    """
    Scrapes a webpage for 'a' tags with rel='bookmark' inside a specific div.
    Args:
        url (str): The URL of the webpage to scrape.
        client (httpx.AsyncClient): Shared async HTTP client.
    """
    try:
        await asyncio.sleep(1.5)
        response = await client.get(url, timeout=10)
        response.raise_for_status()
    except httpx.HTTPError as e:
        print(f"Error fetching the URL: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    target_div = soup.find('div', id='tdi_93')

    if not target_div:
        print("Could not find the div with id='tdi_93' on the page.")
        return None

    bookmark_links = target_div.select('#tdi_93 div.td-module-meta-info > h3 > a')

    if not bookmark_links:
        print("No bookmark links found inside the target div.")
        return None

    print(f"Found {len(bookmark_links)} bookmark links:")
    links = []
    for link in bookmark_links:
        href = link.get('href', 'No URL found')
        text = link.text.strip()
        print(f"- Text: {text} | URL: {href}")
        links.append(href)
    return links