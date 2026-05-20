import asyncio
import random
from typing import Optional

import httpx
import math
from bs4 import BeautifulSoup, NavigableString

_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/120.0.0.0 Safari/537.36'
}

_SENTINEL = "Na·simang iakoba nina man·gen:"


async def scrape_bookmark_articles(article_url: str, client: httpx.AsyncClient) -> list[Optional[str]]:
    """
    Takes an article URL, extracts paragraph text, and returns a list of paragraph strings.
    """
    print(f"Fetching article page: {article_url}")
    final_paragraphs = []
    try:
        await asyncio.sleep(1.5 + 10*random.random())
        response = await client.get(article_url, headers=_HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.select('[data-td-block-uid="tdi_106"] > div.tdb-block-inner.td-fix-index > p')
        for paragraph in paragraphs:
            if paragraph.get_text(strip=True) == _SENTINEL:
                break
            text = "".join(
                node.strip()
                for node in paragraph.contents
                if isinstance(node, NavigableString)
            ).strip()
            final_paragraphs.append(text)
    except httpx.HTTPError as e:
        print(f" -> Error fetching article: {e}")
    return final_paragraphs