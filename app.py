from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = FastAPI()

class CrawlRequest(BaseModel):
    urls: list=[]

@app.post("/extract_product_urls")
def extract_product_urls(crawl_request: CrawlRequest):
   
    try:
        print(f"crawl_request.url: {crawl_request.urls}")
        session = requests.Session()
        response = session.get(crawl_request.urls)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))

    soup = BeautifulSoup(response.content, 'html.parser')

    # Adjust selectors based on the website's actual HTML structure
    product_links = soup.find_all('a', attrs={'class': 'uiv2-product-title'})

    product_urls = []
    for link in product_links:
        href = link.get('href')
        if href:
            full_url = urljoin(crawl_request.url, href)
            product_urls.append(full_url)

    return {"product_urls": product_urls}

@app.get("/")
def read_root():
    return {"Hello": "World"}