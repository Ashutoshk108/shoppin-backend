# app/main.py

from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from typing import List
import json

from .models import CrawlRequest, CrawlResult
from .crawler import crawl_domains

app = FastAPI(
    title="E-commerce Product URL Crawler",
    description="A FastAPI-based web crawler to discover and list product URLs across multiple e-commerce websites.",
    version="1.0.0"
)

@app.post("/extract_product_urls", response_model=CrawlResult)
async def extract_product_urls(crawl_request: CrawlRequest):
    try:
        domains = [str(domain).replace("http://", "").replace("https://", "").rstrip('/') for domain in crawl_request.domains]
        if not domains:
            raise HTTPException(status_code=400, detail="No domains provided.")
        crawl_result = await crawl_domains(domains)
        
        with open('output/product_urls.json', 'w') as f:
            json.dump(crawl_result, f, indent=4)
        
        return CrawlResult(product_urls=crawl_result)
    
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Welcome to the E-commerce Product URL Crawler API!"}