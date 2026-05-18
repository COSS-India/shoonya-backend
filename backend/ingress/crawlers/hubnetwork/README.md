# HubNetwork Crawler

Scrapes Garo-language article text from the HubNetwork site in three stages.

## Pipeline

```
link_collector.scrape_links(url)
    → list[article_url]

extractor.scrape_bookmark_articles(article_url)
    → list[paragraph_str]   (called per URL)

dumps.dump_to_local_fs(sentences_list)
    → data/garo_dump.csv
```

## Modules

### `link_collector.py`
`scrape_links(url) -> list[str] | None`

GETs a listing page, parses with BeautifulSoup, finds `div#tdi_93`, and extracts article hrefs via selector `#tdi_93 div.td-module-meta-info > h3 > a`. Returns `None` on request failure or no matches.

### `extractor.py`
`scrape_bookmark_articles(article_url) -> list[str]`

GETs a single article with a browser User-Agent and a 1.5 s polite delay. Selects paragraphs via `[data-td-block-uid="tdi_106"] > div.tdb-block-inner.td-fix-index > p`, stops at the sentinel string `"Na·simang iakoba nina man·gen:"`, strips inline `<strong>` tags, and returns bare paragraph strings.

### `dumps.py`
`dump_to_local_fs(sentences_list) -> None`

Wraps the flat string list into a pandas DataFrame (`garo_raw` column) and writes `data/garo_dump.csv`.

## Dependencies
`requests`, `beautifulsoup4`, `pandas`