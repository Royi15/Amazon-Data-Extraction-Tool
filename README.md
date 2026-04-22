# Amazon Data Extraction Tool

***Overview***
A Python-based web scraper designed to extract real-time product data from Amazon. This tool automates the process of navigating through multiple search result pages, handling dynamic content, and structuring raw web data into a clean, analysis-ready CSV format.


***Key Features***
* *Dynamic Content Rendering:* Leverages Playwright to simulate a real browser environment, ensuring that lazy-loaded elements and JavaScript-rendered content are fully captured.

* *Intelligent Parsing:* Uses BeautifulSoup with advanced CSS selectors to isolate product attributes with high precision.

* *Automated Pagination:* Built-in logic to navigate across multiple result pages seamlessly.

* *Data Validation Pipeline:* Implements a strict validation layer to filter out noise (like ads or incomplete listings) while maintaining data integrity for new products.


***Technical Stack***
* *Python:* Core logic and data processing.

* *Playwright:* Chromium automation for bypassing basic bot detection and rendering JS.

* *BeautifulSoup4:* HTML parsing and data extraction.

* *CSV Module:* Data persistence and structuring.


***Data Architecture & Logic***
To ensure a high-quality dataset, the script applies the following rules:

* *Mandatory Fields:* Every entry must contain a Title, Price, and Product URL. Entries missing these core attributes (often sponsored banners or layout artifacts) are automatically discarded.

* *Graceful Handling of Nulls:* For attributes like Ratings and Review Counts (which may be missing for new arrivals), the script assigns "N/A" values rather than breaking the flow or omitting the product.


***How to run***
1.**Install Requirements:**
Make sure you have Python installed, then run the following commands from the project directory:
* pip install -r requirements.txt
* playwright install chromium

2.**Execute the Script:**
* python scraper.py

3.**Output:** The data will be saved to amazon_products.csv in the same directory.