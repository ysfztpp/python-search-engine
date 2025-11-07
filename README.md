# My Minimalistic Seach Engine Project Inspired by PageRank Algorithm for DSAI 301

Course project for **DSAI 301 – Introduction to Translation, Bogaziçi University**.

## PageRank Overview

The ranking function mirrors the classic PageRank iteration:
<img width="701" height="239" alt="image" src="https://github.com/user-attachments/assets/bb263d56-6533-452a-aff1-78c40c1ff177" />

Pages with no outgoing links distribute their score uniformly across all pages, matching the “random surfer” interpretation taught in class.

## Running the Demo

```bash
python3 app.py <seed-url> <keyword> [--limit N]
```

Example values:
- `seed-url`: first page to crawl (e.g., `https://example.com`)
- `keyword`: term to look for across the crawled pages
- `--limit`: number of ranked matches printed (default 10)

No external libraries are needed; the entire implementation lives in `app.py`.

## Code Walkthrough

- **Fetching (`get_page`)** – Downloads HTML via `urllib.request`. Network errors simply return an empty string to keep the crawl moving.
- **Cleaning (`get_clear_page`)** – Recreates the original assignment logic by stitching together the `<title>` and `<body>` sections and stripping tags manually.
- **Link graph (`get_all_links`, `union`)** – Finds every `<a href="">` target and expands the crawl frontier without duplicates.
- **Indexing (`add_page_to_index`, `lookup`)** – Builds an inverted index where each lowercase token maps to the URLs that contain it.
- **Crawling (`crawl_web`)** – Depth-first crawl starting from the seed, collecting page text, outgoing links, and the site graph.
- **Ranking (`compute_ranks`, `ranked_lookup`)** – Implements the PageRank-style scoring and sorts query matches by their scores before printing.

