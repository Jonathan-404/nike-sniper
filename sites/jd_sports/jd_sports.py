from sites.jd_sports.scarpe_functions import scrape_product_price, scrape_product_image, scrape_product_sizes
from webhook_manager import webhook_send
from bs4 import BeautifulSoup
import requests

"""
SITE ALGORITHM STARTS HERE

SITE NAME: jd_sports
"""


def new_product_urls(url: str, keywords: list):
    product_urls_file = open("./product_urls.txt", "r")
    product_urls = product_urls_file.read().split('\n')
    product_urls_file.close()

    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')
    product_parents = soup.find_all('div', class_='product-item-meta')

    for product_children in product_parents:
        product_name = product_children.find('h2', class_='product-item-meta__title').text.strip()
        for keyword in keywords:
            if keyword in product_name:

                product_id = product_children.find('h2', class_='product-item-meta__title').get('href').split('/')[-1]
                product_url = f"https://www.jdsports.co.il/products/{product_id}"

                if product_url not in product_urls:
                    product_urls.append(product_url)
                    webhook_send("JD Sports", product_name, product_url, scrape_product_price(product_url), "In Stock", scrape_product_sizes(product_url), scrape_product_image(product_url))
                break

    product_urls_file = open("./product_urls.txt", "w")
    for product_url in product_urls:
        product_urls_file.write(product_url + "\n")
    product_urls_file.close()
