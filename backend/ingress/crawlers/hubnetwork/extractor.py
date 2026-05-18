import time
from typing import Optional

import requests
from bs4 import BeautifulSoup, NavigableString


def scrape_bookmark_articles(article_url: str) -> list[Optional[str]]:
    """
    Takes an article's url at a time, extracts the languages and returns a list of chunked paragraphs.
    at this stage processing do not output a single string.
    """
    # 1. Use a standard User-Agent. Many sites block requests without one.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/120.0.0.0 Safari/537.36'
    }
    print(f"Fetching article page: {article_url}")
    final_paragraphs = []
    try:
        # 2. Be polite! Add a delay so you don't DDoS the server.
        time.sleep(1.5)
        article_response = requests.get(article_url, headers=headers, timeout=10)
        article_response.raise_for_status()
        article_soup = BeautifulSoup(article_response.text, 'html.parser')
        paragraphs = article_soup.select('[data-td-block-uid="tdi_106"]>div.tdb-block-inner.td-fix-index>p')
        for paragraph in paragraphs:
            if paragraph.get_text(strip=True) == "Na·simang iakoba nina man·gen:":
                break
            text_outside_strong = "".join(
                text.strip()
                for text in paragraph.contents
                if isinstance(text, NavigableString)
            ).strip()
            final_paragraphs.append(text_outside_strong)
    except requests.exceptions.RequestException as e:
        print(f" -> Error fetching article: {e}")
    return final_paragraphs
