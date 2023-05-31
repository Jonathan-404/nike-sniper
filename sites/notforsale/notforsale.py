from sites.notforsale.scarpe_functions import scrape_product_image, scrape_product_sizes
from webhook_manager import new_shoe_message
from bs4 import BeautifulSoup
import requests
import json



"""
SITE ALGORITHM STARTS HERE

SITE NAME: not for sale
"""

def new_product_urls(url: str, keywords: list):
    pages = [url + '1']
    product_urls = []
    product_data_file = json.load(open("product_data.json", "r"))
    for product in product_data_file["notforsale"]:
        product_urls.append(product["product_url"])

    content = requests.get(url + '1').content
    soup = BeautifulSoup(content, 'html.parser')
    page_num = int(soup.find('div', class_='pagination').find('a').text)

    for page in range(1, page_num + 1):
        pages.append(f'{url}{page}')

    for page in pages:
        content = requests.get(page).content
        soup = BeautifulSoup(content, 'html.parser')
        product_parent = soup.find_all('div', class_='grid-product__content')
        for product_child in product_parent:
            product_url = f"https://notforsaletlv.com/{product_child.find('a')['href']}"
            product_image = f"https:{product_child.find('img')['src']}"
            product_name = f"{product_child.find('div', class_='grid-product__meta').find('div', class_='grid-product__vendor').text.strip()} {product_child.find('div', class_='grid-product__meta').find('div', class_='grid-product__title grid-product__title--heading').text.strip()}"
            product_price = product_child.find('div', class_='grid-product__price').text.strip().split('\n')
            if "Regular price" in product_price:
                product_price = product_price[2][10:]
            else:
                product_price = product_price[0]

            for keyword in keywords:
                if keyword in product_name:
                    product_content = requests.get(product_url).content
                    product_soup = BeautifulSoup(product_content, 'html.parser')

                    # store product data in json file
                    product_data = {
                        "product_name": product_name,
                        "product_url": product_url,
                        "product_price": product_price,
                        "product_stock": "In Stock",
                        "product_sizes": ['12'],
                        "product_image": product_image
                    }
                    # send product data to webhook
                    if product_data["product_url"] not in product_urls:
                        product_urls.append(product_url)

                        product_urls.append(product_data["product_url"])
                        update_products_json_file("notforsale", product_data)
                        new_shoe_message("Notforsale", product_data["product_name"],
                                         product_data["product_url"],
                                         product_data["product_price"], "In Stock", product_data["product_sizes"],
                                         product_data["product_image"])


            # get the link of every shoe in the site

def update_products_json_file(company_name: str, product_data: dict):
    with open("product_data.json", 'r+') as file:
        file_data = json.load(file)
        file_data[company_name].append(product_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)