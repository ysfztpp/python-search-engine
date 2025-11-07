# DSAI 301 Search Engine

Course project for **DSAI 301 – Introduction to Translation, Bogaziçi University**. The goal is to show how a minimal crawler plus PageRank-inspired ranking can deliver meaningful search results even with a tiny amount of Python code.

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

## PageRank Overview

The ranking function mirrors the classic PageRank iteration:

\[
\text{rank}_{t+1}(p) = \frac{1-d}{N} + d \sum_{q \to p} \frac{\text{rank}_t(q)}{L(q)}
\]

- \( d = 0.8 \) is the damping factor (probability of following a link).
- \( N \) is the number of pages in the crawl.
- \( q \to p \) means page \( q \) links to \( p \).
- \( L(q) \) is the number of outgoing links from \( q \).

Pages with no outgoing links distribute their score uniformly across all pages, matching the “random surfer” interpretation taught in class.

## Repository Layout

```
.gitignore      # Keeps caches and OS files out of version control
app.py          # Complete crawler + indexer + PageRank + CLI
README.md       # Course-focused documentation (images can be added here)
```
