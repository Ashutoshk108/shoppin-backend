# E-commerce Product URL Crawler

## Overview

This project is a FastAPI-based web crawler designed to discover and list all product URLs across multiple e-commerce websites. It accepts a list of domains and outputs a structured list mapping each domain to its discovered product URLs.

## Features

- **URL Discovery:** Utilizes pattern-based strategies to identify product pages.
- **Scalability:** Handles multiple domains concurrently using asynchronous processing.
- **Performance:** Employs `aiohttp` and `asyncio` for efficient crawling.
- **Robustness:** Includes error handling, respects `robots.txt`, and manages dynamic content with Playwright.
- **Structured Output:** Outputs results in a clear JSON format mapping each domain to its product URLs.

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/ecommerce_crawler.git
    cd ecommerce_crawler
    ```

2. **Set Up Virtual Environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Install Playwright Browsers:**

    ```bash
    playwright install
    ```

## Usage

1. **Run the FastAPI Application:**

    ```bash
    uvicorn app.main:app --reload
    ```

    The API will be accessible at `http://127.0.0.1:8000`.

2. **API Endpoint**

    - **POST** `/extract_product_urls`

    **Request Body:**

    ```json
    {
        "domains": [
            "https://example1.com",
            "https://example2.com",
            "https://example3.com"
        ]
    }
    ```

    **Response:**

    ```json
    {
        "product_urls": {
            "example1.com": [
                "https://example1.com/product/12345",
                "https://example1.com/product/67890"
            ],
            "example2.com": [
                "https://example2.com/item/abcde",
                "https://example2.com/item/fghij"
            ],
            "example3.com": [
                "https://example3.com/p/xyz",
                "https://example3.com/p/uvw"
            ]
        }
    }
    ```

3. **Example Using `curl`:**

    ```bash
    curl -X POST "http://127.0.0.1:8000/extract_product_urls" \
    -H "Content-Type: application/json" \
    -d '{
        "domains": [
            "https://example1.com",
            "https://example2.com",
            "https://example3.com"
        ]
    }'
    ```

## Configuration

- **Crawler Settings:** Modify `crawler.py` to adjust crawling behavior, such as `max_pages`, `REQUEST_DELAY`, and `PRODUCT_URL_PATTERNS`.
- **Concurrency:** Fine-tune the number of concurrent requests based on your system's capabilities and target website policies.
  
## Data Output

- **Structured JSON:** The crawler saves the results to `output/product_urls.json` in the following format:

    ```json
    {
        "example1.com": [
            "https://example1.com/product/12345",
            "https://example1.com/product/67890"
        ],
        "example2.com": [
            "https://example2.com/item/abcde",
            "https://example2.com/item/fghij"
        ]
        // ...
    }
    ```

## Contribution

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.