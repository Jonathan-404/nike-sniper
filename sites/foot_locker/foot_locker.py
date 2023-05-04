from sites.foot_locker.scarpe_functions import scrape_product_price, scrape_product_image, scrape_product_sizes
from webhook_manager import new_shoe_message
from bs4 import BeautifulSoup
import requests
import json

"""
SITE ALGORITHM STARTS HERE

SITE NAME: Foot Locker
"""


def new_product_urls(url: str, keywords: list):
    pass


def update_products_json_file(company_name: str, product_data: dict):
    with open("product_data.json", 'r+') as file:
        file_data = json.load(file)
        file_data[company_name].append(product_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)
