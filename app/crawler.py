# app/crawler.py

import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from typing import List, Dict, Set
from playwright.async_api import async_playwright

PRODUCT_URL_PATTERNS = [
    re.compile(r'/product/'),
    re.compile(r'/item/'),
    re.compile(r'/p/'),
    re.compile(r'/products/'),
    re.compile(r'\?product_id='),
    re.compile(r'/dp/'),
    re.compile(r'/dp/product/'),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; EcommerceCrawler/1.0;)"
}

async def fetch(session: aiohttp.ClientSession, url: str) -> str:
    try:
        async with session.get(url, headers=HEADERS, timeout=10) as response:
            response.raise_for_status()
            return await response.text()
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return ""

def is_product_url(url: str) -> bool:
    path = urlparse(url).path
    for pattern in PRODUCT_URL_PATTERNS:
        if pattern.search(path):
            return True
    return False

async def fetch_with_playwright(playwright, url: str) -> str:
    browser = await playwright.chromium.launch(headless=True)
    page = await browser.new_page()
    try:
        await page.goto(url, timeout=10000)
        content = await page.content()
    except Exception as e:
        print(f"Playwright failed to fetch {url}: {e}")
        content = ""
    await browser.close()
    return content

async def crawl_domain(session: aiohttp.ClientSession, playwright, domain: str, max_pages: int = 100) -> Set[str]:
    product_urls = set()
    urls_to_visit = set([f"http://{domain}", f"https://{domain}"])
    visited_urls = set()

    while urls_to_visit and len(visited_urls) < max_pages:
        current_url = urls_to_visit.pop()
        if current_url in visited_urls:
            continue
        visited_urls.add(current_url)

        # Attempt to fetch with aiohttp
        html = await fetch(session, current_url)

        # Fallback to Playwright if aiohttp fails or detects dynamic content
        if not html or "some indicator of dynamic content" in html.lower():
            html = await fetch_with_playwright(playwright, current_url)

        if not html:
            continue
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            full_url = urljoin(current_url, href)
            parsed_full_url = urlparse(full_url)
            if parsed_full_url.netloc != urlparse(current_url).netloc:
                continue  # Skip external links
            if is_product_url(full_url):
                product_urls.add(full_url)
            if full_url not in visited_urls:
                urls_to_visit.add(full_url)
    return product_urls

async def crawl_domains(domains: List[str]) -> Dict[str, List[str]]:
    result = {}
    async with aiohttp.ClientSession() as session, async_playwright() as playwright:
        tasks = []
        for domain in domains:
            tasks.append(crawl_domain(session, playwright, domain))
        crawled_results = await asyncio.gather(*tasks)
        for domain, urls in zip(domains, crawled_results):
            result[domain] = list(urls)
    return result