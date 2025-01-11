# app/crawler.py

import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from typing import List, Dict, Set

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

async def crawl_domain(session: aiohttp.ClientSession, domain: str, max_pages: int = 100) -> Set[str]:
    product_urls = set()
    urls_to_visit = set([f"http://{domain}", f"https://{domain}"])
    visited_urls = set()

    while urls_to_visit and len(visited_urls) < max_pages:
        current_url = urls_to_visit.pop()
        if current_url in visited_urls:
            continue
        visited_urls.add(current_url)

        # Fetch page content
        html = await fetch(session, current_url)

        if not html:
            continue

        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            full_url = urljoin(current_url, href)
            parsed_full_url = urlparse(full_url)
            
            # Skip external links
            if parsed_full_url.netloc != urlparse(current_url).netloc:
                continue
            
            # Identify product URLs
            if is_product_url(full_url):
                product_urls.add(full_url)
            
            # Add to urls to visit
            if full_url not in visited_urls:
                urls_to_visit.add(full_url)
    
    return product_urls

async def crawl_domains(domains: List[str]) -> Dict[str, List[str]]:
    result = {}
    async with aiohttp.ClientSession() as session:
        tasks = []
        for domain in domains:
            tasks.append(crawl_domain(session, domain))
        
        crawled_results = await asyncio.gather(*tasks)
        
        for domain, urls in zip(domains, crawled_results):
            result[domain] = list(urls)
    
    return result