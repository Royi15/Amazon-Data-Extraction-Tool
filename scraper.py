import csv
import time
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def scrape_amazon_page(url):
    with sync_playwright() as p:
        # we are setting up a website to scrape the data like a normal user
        browser = p.chromium.launch(headless=False) 

        # we are opening a new page and navigating to the target URL
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded")

        # Wait for the product listings to load
        page.wait_for_timeout(5000)

        # we scroll down to avoid lazy loading and ensure all products are loaded on the page
        for _ in range(10):
            page.mouse.wheel(0, 500) 
            page.wait_for_timeout(1500)
        
        # we extract the HTML content
        html = page.content()

        browser.close()

        return html
    
def parse_results(html):
    soup = BeautifulSoup(html, 'html.parser')
    products = []
    
    # we go through the HTML and take all the components that have the type of a product
    products = soup.select('div.s-result-item.s-asin')

    products_data = []

    for product in products:
        try:
            # the title of the product is under an h2 div 
            title = product.select_one('h2').text.strip()

            # the price of the product is under a div with the class a-price and a-offscreen
            price = product.select_one('.a-price .a-offscreen').text.strip()
            

            # we try to get the rating of the product; if it is not available, we set it to "N/A"
            # this is categorized as an optional field (see explanation in the README)
            # by doing this, the code handles missing data gracefully without skipping the product
            rating_check = product.select_one('.a-row.a-size-small .a-size-small.a-color-base')
            rating = rating_check.text.strip() if rating_check else "N/A"

            # We try to get the review count; if it is not available, we set it to "N/A"
            # Categorized as an optional field to ensure new products are still captured
            review_count_check =product.select_one('.a-size-mini.puis-normal-weight-text.s-underline-text')
            review_count = review_count_check.text.replace('(', '').replace(')', '').strip() if review_count_check else "N/A"

            # the URL of the product is under an a tag with the class a-link-normal
            productURL = 'https://www.amazon.com' + product.select_one('a.a-link-normal')['href']

            products_data.append([title, price, rating, review_count, productURL])
        except Exception as e:
            # we continue even if some products are broken(eg, diffrent HTML structure)
            print(f"[INFO] Ignored an item: HTML structure does not match a standard product.")
            continue

    return products_data

def save_to_csv(data, filename="amazon_products.csv"):
    # export the scraped data to a CSV file
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # write column headers
        writer.writerow(['Title', 'Price', 'Rating', 'Review Count', 'Product URL'])
        
        # write all product data rows
        writer.writerows(data)
        


url = 'https://www.amazon.com/s?i=videogames-intl-ship&srs=16225016011&rh=n%3A16225016011&s=popularity-rank&fs=true&qid=1776861552&xpid=Ezv7nHIwvGH6m&ref=sr_pg_1'
all_products_data = []

print("Extracting data from Amazon, please hold on...")
for page_num in range(1, 3):
    # we are iterating through the first 2 pages of the search results
    current_url = f"{url}&page={page_num}"

    # we scrape the current page and parse the results
    HTML = scrape_amazon_page(current_url)

    # we extract the product data from the HTML and add it to our list of all products
    products_data = parse_results(HTML)
    all_products_data.extend(products_data)

    if page_num < 2:
        # we wait for 3 seconds because the code is making the requests very fast,
        #and we want to avoid getting blocked by Amazon 
        time.sleep(3)

save_to_csv(all_products_data)
print("Finished! Check the CSV file for the scraped data.")





