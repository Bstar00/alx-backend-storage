#!/usr/bin/env python3
"""It implement an expiring web cache and tracker to obtain HTML content of a URL."""
import redis
import requests

r = redis.Redis()


def fetch_page(url: str) -> str:
    """Fetch a web page, track access count, and cache with expiration."""
    page_count_key = f"count:{url}"
    cached_page_key = f"cached:{url}"

    """Increment access count"""
    r.incr(page_count_key)

    """Try to retrieve cached HTML"""
    cached_html = r.get(cached_page_key)
    if cached_html:
        return cached_html.decode('utf-8')

    """ Fetch the page if not in cache"""
    response = requests.get(url)
    html_content = response.text

    """ Cache the HTML with expiration"""
    r.setex(cached_page_key, 10, html_content)

    return html_content


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
