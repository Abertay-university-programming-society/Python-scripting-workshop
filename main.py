import requests
from lxml import html
from bs4 import BeautifulSoup

def script(url):

    page_count = 23
    for page in range(1, page_count): 
        full_url = f"{url}?page={page}"
        request = requests.get(full_url)
        print(full_url)
        soup = BeautifulSoup(request.text, 'html.parser')
        items = soup.find_all("div", class_="product-item")
        for item in items:
            price = item.find("span", class_="price price--highlight")
            name = item.find("a", class_="product-item__title text--strong link")
            stock = item.find("span", class_="product-item__inventory inventory inventory--high")
            try:
                row = price.text, name.text, stock.text
                print(row) 
            except Exception as e:
                print(e)
                continue

            
if __name__ == '__main__':
    url = 'https://www.books4people.co.uk/collections/product-0-to-5'
    script(url)