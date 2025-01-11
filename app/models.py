# app/models.py

from typing import List, Dict
from pydantic import BaseModel, HttpUrl

class CrawlRequest(BaseModel):
    domains: List[HttpUrl]

class CrawlResult(BaseModel):
    product_urls: Dict[str, List[HttpUrl]]