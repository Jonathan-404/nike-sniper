from src.factory_54.scrape_functions import scrape_product_sizes
from webhook_manager import new_shoe_message
from bs4 import BeautifulSoup
import requests
import json

"""
SITE ALGORITHM STARTS HERE

SITE NAME: Factory 54
"""

factory_api = "https://www.factory54.co.il/on/demandware.store/Sites-factory54-Site/iw_IL/Product-Variation?pid="

def new_product_urls(urls: list, keywords: list):
    for url in urls:
        start_param = 0
        for i in range(15):

            product_urls = []

            product_data_file = json.load(open("product_data.json", "r"))
            for product in product_data_file["factory_54"]:
                product_urls.append(product["product_url"])

            content = requests.get(url + str(start_param)).content
            soup = BeautifulSoup(content, 'html.parser')
            product_parents = soup.find_all('div', class_='present-product product also-like__img')
            for product_children in product_parents:
                product_name = f"""{json.loads(product_children.get("data-gtm-product"))["item_name"]} {json.loads(product_children.get("data-gtm-product"))["item_brand"]} {json.loads(product_children.get("data-gtm-product"))["item_variant"]}"""
                product_price = json.loads(product_children.get("data-gtm-product"))["price"]
                product_image = product_children.find('img', class_='tile-image also-like__img--tile primary-image').get('src')
                product_url = product_children.find('a', class_='link tile-body__product-name').get('href')
                product_id = product_children.get('data-pid')

                for keyword in keywords:
                    if keyword in product_name:

                        product_content = requests.get(f"{factory_api}{product_id}").content
                        # store product data in json file
                        product_data = {
                            "product_name": product_name,
                            "product_url": product_url,
                            "product_price": product_price,
                            "product_stock": "In Stock",
                            "product_sizes": scrape_product_sizes(product_content),
                            "product_image": product_image
                        }
                        if product_data["product_url"] not in product_urls:
                            product_urls.append(product_data["product_url"])
                            new_shoe_message("Factory 54", product_data["product_name"], product_data["product_url"], product_data["product_price"], "In Stock", product_data["product_sizes"], product_data["product_image"])
                            update_products_json_file("factory_54", product_data)

                        start_param += 48

                        break


def update_products_json_file(company_name: str, product_data: dict):
    with open("product_data.json", 'r+') as file:
        file_data = json.load(file)
        file_data[company_name].append(product_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)