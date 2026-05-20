import asyncio
from time import sleep

import httpx

from dumps import dump_to_local_fs
from extractor import scrape_bookmark_articles
from link_collector import scrape_links


async def _run(url: str) -> list[str]:
    async with httpx.AsyncClient() as client:
        article_urls = await scrape_links(url, client)
        if not article_urls:
            print("No article URLs collected. Aborting.")
            return []

        tasks = [scrape_bookmark_articles(article_url, client) for article_url in article_urls]
        results = await asyncio.gather(*tasks)

    sentences = [paragraph for paragraphs in results for paragraph in paragraphs if paragraph]
    return sentences


def orchestrate_pipeline(url: str, start_page, end_page, page_interval_time=2) -> None:
    sentences = []
    for i in range(start_page,end_page):
        sleep(page_interval_time)
        sentences += asyncio.run(_run(url.format(i)))
    dump_to_local_fs(sentences)


if __name__ == "__main__":
    orchestrate_pipeline("https://hubnetwork.in/category/garo/page/{}/", 501, 1000)
