from sites.jd_sports.scarpe_functions import scrape_product_price, scrape_product_image, scrape_product_sizes
from webhook_manager import new_shoe_message
from bs4 import BeautifulSoup
import requests
import json

"""
SITE ALGORITHM STARTS HERE

SITE NAME: JD Sports
"""


def new_product_urls(url: str, keywords: list):
    for i in range(12):
        product_urls = []

        product_data_file = json.load(open("./product_data.json", "r"))
        for product in product_data_file["jd_sports"]:
            product_urls.append(product["product_url"])

        content = requests.get(url + str(i)).content
        soup = BeautifulSoup(content, 'html.parser')
        product_parents = soup.find_all('div', class_='product-item-meta')

        for product_children in product_parents:
            product_name = product_children.find('h2', class_='product-item-meta__title').text.strip()
            for keyword in keywords:
                if keyword in product_name:

                    product_id = product_children.find('h2', class_='product-item-meta__title').get('href').split('/')[-1]
                    product_url = f"https://www.jdsports.co.il/products/{product_id}".strip()

                    product_content = requests.get(product_url).content
                    product_soup = BeautifulSoup(product_content, 'html.parser')

                    # store product data in json file
                    product_data = {
                        "product_name": product_name,
                        "product_url": product_url,
                        "product_price": scrape_product_price(product_soup),
                        "product_stock": "In Stock",
                        "product_sizes": scrape_product_sizes(product_soup),
                        "product_image": scrape_product_image(product_soup)
                    }

                    if product_data["product_url"] not in product_urls:
                        product_urls.append(product_data["product_url"])
                        new_shoe_message("JD Sports", product_data["product_name"], product_data["product_url"], product_data["product_price"], "In Stock", product_data["product_sizes"], product_data["product_image"])
                        update_products_json_file("jd_sports", product_data)

                    break


def update_products_json_file(company_name: str, product_data: dict):
    with open("product_data.json", 'r+') as file:
        file_data = json.load(file)
        file_data[company_name].append(product_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)
