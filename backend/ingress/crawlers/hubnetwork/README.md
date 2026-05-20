# HubNetwork Crawler

Scrapes Garo-language article text from the HubNetwork site in three stages.

## Pipeline

```
# 1. Collect article URLs (async)
article_urls = await link_collector.scrape_links(url)
    → list[article_url]

# 2. Scrape all articles concurrently (async, httpx)
tasks = [extractor.scrape_bookmark_articles(url) for url in article_urls]
results = await asyncio.gather(*tasks)
    → list[list[paragraph_str]]

# 3. Flatten all paragraphs into a single list
sentences_list = [p for paragraphs in results for p in paragraphs]
    → list[str]

# 4. Exit the event loop, then write to disk (sync)
asyncio.run(main())
dumps.dump_to_local_fs(sentences_list)
    → data/garo_dump.csv
```

## Modules

### `link_collector.py`
`async scrape_links(url) -> list[str] | None`

GETs a listing page using an `httpx.AsyncClient`, parses with BeautifulSoup, finds `div#tdi_93`, and extracts article hrefs via selector `#tdi_93 div.td-module-meta-info > h3 > a`. Returns `None` on request failure or no matches.

### `extractor.py`
`async scrape_bookmark_articles(article_url) -> list[str]`

GETs a single article using a shared `httpx.AsyncClient` with a browser User-Agent and a 1.5 s polite delay (`asyncio.sleep`). Selects paragraphs via `[data-td-block-uid="tdi_106"] > div.tdb-block-inner.td-fix-index > p`, stops at the sentinel string `"Na·simang iakoba nina man·gen:"`, strips inline `<strong>` tags, and returns bare paragraph strings.

All article URLs are fetched concurrently via `asyncio.gather`. Once all coroutines resolve, their results are flattened into a single `list[str]` before the event loop exits.

### `dumps.py`
`dump_to_local_fs(sentences_list) -> None`

Wraps the flat string list into a pandas DataFrame (`garo_raw` column) and writes `data/garo_dump.csv`. Called synchronously after `asyncio.run` returns.

## Dependencies
`httpx`, `beautifulsoup4`, `pandas`