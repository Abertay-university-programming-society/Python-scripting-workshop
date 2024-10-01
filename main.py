import aiohttp  # Import aiohttp to handle asynchronous HTTP requests
import asyncio  # Import asyncio to manage asynchronous tasks
from bs4 import BeautifulSoup  # Import BeautifulSoup to parse HTML content

# Define a class for scraping product information from the website
class ProductScraper:
    # Initialize the scraper with the base URL and number of pages to scrape
    def __init__(self, base_url, page_count=23):
        self.base_url = base_url  # Store the base URL for the product pages
        self.page_count = page_count  # Define how many pages we want to scrape

    # Async method to fetch a specific page content
    async def fetch_page(self, session, page):
        # Construct the full URL by appending the page number to the base URL
        full_url = f"{self.base_url}?page={page}"
        # Use aiohttp's session to make an asynchronous GET request to the URL
        async with session.get(full_url) as response:
            print(f"Fetching: {full_url}")  # Print which page we're fetching (for logging purposes)
            # Return the text (HTML content) of the response asynchronously
            return await response.text()

    # Async method to parse the HTML content of a page and extract product info
    async def parse_page(self, html_content):
        # Use BeautifulSoup to parse the HTML content we received from the page
        soup = BeautifulSoup(html_content, 'html.parser')
        # Find all div elements with the class "product-item" which contain the product info
        items = soup.find_all("div", class_="product-item")
        # Initialize an empty list to store the extracted product data
        product_data = []
        # Loop through each product item found on the page
        for item in items:
            try:
                # Try to extract the price, name, and stock status of each product
                price = item.find("span", class_="price price--highlight").text
                name = item.find("a", class_="product-item__title text--strong link").text
                stock = item.find("span", class_="product-item__inventory inventory inventory--high").text
                # Append the extracted data (name, price, stock) as a tuple to the product_data list
                product_data.append((name, price, stock))
            except AttributeError:
                # If any of the above fields (price, name, or stock) are missing, skip this item
                continue
        # Return the list of extracted product data
        return product_data

    # Async method to manage the whole scraping process
    async def scrape(self):
        # Open an asynchronous session with aiohttp for making HTTP requests
        async with aiohttp.ClientSession() as session:
            # Initialize an empty list to hold our fetch tasks (one for each page)
            tasks = []
            # Loop through the pages we want to scrape (from page 1 to page_count)
            for page in range(1, self.page_count + 1):
                # Append each fetch task to the tasks list (these will be run concurrently)
                tasks.append(self.fetch_page(session, page))

            # Run all the fetch tasks concurrently and wait for them to finish
            pages_content = await asyncio.gather(*tasks)

            # Initialize an empty list to store all the products across all pages
            all_products = []
            # Loop through the content of each fetched page
            for content in pages_content:
                # Parse the page and extract the product info
                products = await self.parse_page(content)
                # Add the extracted products to the all_products list
                all_products.extend(products)

            # Return the complete list of all products scraped from all pages
            return all_products


# Main function to execute the scraping process
async def main():
    # Define the base URL for the product pages we want to scrape
    url = 'https://www.books4people.co.uk/collections/product-0-to-5'
    # Instantiate the ProductScraper class with the base URL
    scraper = ProductScraper(url)
    # Run the scrape method asynchronously and collect the scraped product data
    products = await scraper.scrape()

    # Loop through the scraped products and print them out
    for product in products:
        print(product)


# If this script is being run directly (not imported), run the main function
if __name__ == '__main__':
    # Use asyncio to run the main function, which is asynchronous
    asyncio.run(main())
