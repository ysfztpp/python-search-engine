import argparse
from urllib import error, request


def get_page(url):
    try:
        with request.urlopen(url, timeout=10) as response:
            return response.read().decode("utf-8", errors="ignore")
    except (error.URLError, ValueError, TimeoutError):
        return ""


def strip_tags(text):
    """Remove HTML tags from a string."""
    result = []
    inside_tag = False
    for char in text:
        if char == "<":
            inside_tag = True
            continue
        if char == ">":
            inside_tag = False
            continue
        if not inside_tag:
            result.append(char)
    return "".join(result)


def slice_section(content, tag):
    """Extract text between <tag>...</tag> if present."""
    lower = content.lower()
    open_tag = f"<{tag}>"
    close_tag = f"</{tag}>"
    start = lower.find(open_tag)
    if start == -1:
        return ""
    end = lower.find(close_tag, start)
    if end == -1:
        return ""
    start_index = start + len(open_tag)
    return content[start_index:end]


def get_clear_page(content):
    """Mimic the original title+body extraction while remaining robust."""
    if not content:
        return ""
    title = slice_section(content, "title")
    body = slice_section(content, "body") or content
    cleaned = f"{title} {body}".strip()
    return strip_tags(cleaned)


def get_next_target(page):
    start_link = page.find("<a href=")
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1 : end_quote]
    return url, end_quote


def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links


def union(p, q):
    for e in q:
        if e not in p:
            p.append(e)


def add_to_index(index, keyword, url):
    urls = index.setdefault(keyword, [])
    if url not in urls:
        urls.append(url)


def add_page_to_index(index, url, content):
    for word in content.split():
        keyword = word.lower()
        if keyword:
            add_to_index(index, keyword, url)


def lookup(index, keyword):
    return index.get(keyword.lower(), [])


def crawl_web(seed):
    tocrawl = [seed]
    crawled = set()
    index = {}
    graph = {}
    while tocrawl:
        page = tocrawl.pop()
        if page in crawled:
            continue
        html = get_page(page)
        text = get_clear_page(html)
        links = get_all_links(html)
        add_page_to_index(index, page, text)
        graph[page] = links
        union(tocrawl, links)
        crawled.add(page)
    for node in list(graph):
        graph.setdefault(node, [])
    return index, graph


def compute_ranks(graph):
    d = 0.8
    numloops = 10
    n = len(graph) or 1
    ranks = {page: 1.0 / n for page in graph}
    for _ in range(numloops):
        newranks = {}
        for page in graph:
            rank = (1 - d) / n
            for node, outlinks in graph.items():
                if not outlinks:
                    rank += d * (ranks[node] / n)
                elif page in outlinks:
                    rank += d * (ranks[node] / len(outlinks))
            newranks[page] = rank
        ranks = newranks
    return ranks


def ranked_lookup(index, keyword, graph):
    results = lookup(index, keyword)
    if not results:
        return []
    ranks = compute_ranks(graph)
    ranked = sorted([(ranks.get(url, 0), url) for url in results], reverse=True)
    return [url for _, url in ranked]


def main():
    parser = argparse.ArgumentParser(description="Tiny crawler + search demo.")
    parser.add_argument("seed", help="starting URL to crawl")
    parser.add_argument("keyword", help="keyword to search for")
    parser.add_argument("--limit", type=int, default=10, help="maximum results to show")
    args = parser.parse_args()

    index, graph = crawl_web(args.seed)
    results = ranked_lookup(index, args.keyword, graph)
    if not results:
        print("No matches were found for that keyword.")
        return
    shown = results[: args.limit] if args.limit > 0 else results
    for position, url in enumerate(shown, start=1):
        print(f"{position}. {url}")


if __name__ == "__main__":
    main()
