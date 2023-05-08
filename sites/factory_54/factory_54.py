#from . scrape_functions import scrape_product_price, scrape_product_image, scrape_product_sizes
#from webhook_manager import new_shoe_message
from bs4 import BeautifulSoup
import requests
import json

"""
SITE ALGORITHM STARTS HERE

SITE NAME: Factory 54
"""


def new_product_urls(urls: list, keywords: list):
    for url in urls:
        start_param = 0
        for i in range(15):

            """product_urls = []

            product_data_file = json.load(open("./product_data.json", "r"))
            for product in product_data_file["factory_54"]:
                product_urls.append(product["product_url"])"""

            content = requests.get(url + str(start_param)).content
            soup = BeautifulSoup(content, 'html.parser')
            product_parents = soup.find_all('div', class_='present-product product also-like__img')
            for product_children in product_parents:
                # {"item_id":"850362285-m","item_category5":"850362285","item_name":"נעלי סניקרס מכותנה","item_list_id":"PLP","item_list_name":"Product List Page","item_brand":"VALENTINO GARAVANI","currency":"ILS","item_category":"גברים","item_category2":"נעליים","item_category3":"סניקרס","item_category4":"(not set)","index":"48","item_variant":"כחול","location_id":"(not set)","salePrice":2490,"price":2490}
                #
                product_name = f"""{json.loads(product_children.get("data-gtm-product"))["item_name"]} {json.loads(product_children.get("data-gtm-product"))["item_brand"]} {json.loads(product_children.get("data-gtm-product"))["item_variant"]}"""
                print(product_name)
                """for keyword in keywords:
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
                            new_shoe_message("Factory 54", product_data["product_name"], product_data["product_url"], product_data["product_price"], "In Stock", product_data["product_sizes"], product_data["product_image"])
                            update_products_json_file("factory_54", product_data)

                        start_param += 48

                        break"""


new_product_urls(["https://www.factory54.co.il/men-shoes-sneakers?start="], ["air"])


def update_products_json_file(company_name: str, product_data: dict):
    with open("product_data.json", 'r+') as file:
        file_data = json.load(file)
        file_data[company_name].append(product_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)
