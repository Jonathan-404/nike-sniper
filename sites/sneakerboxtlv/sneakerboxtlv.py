from sites.sneakerboxtlv.scarpe_functions import scrape_product_image, scrape_product_sizes
from webhook_manager import new_shoe_message
from bs4 import BeautifulSoup
import requests
import json

"""
SITE ALGORITHM STARTS HERE

SITE NAME: Sneakerboxtlv
"""


def new_product_urls(url: str, keywords: list):
    cookies = {"tk_or": "%22%22", "tk_r3d": "%22%22", "tk_lr": "%22%22"}
    headers = {"Sec-Ch-Ua": "\"Not:A-Brand\";v=\"99\", \"Chromium\";v=\"112\"", "Accept": "*/*",
                     "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                     "X-Requested-With": "XMLHttpRequest", "Sec-Ch-Ua-Mobile": "?0",
                     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36",
                     "Sec-Ch-Ua-Platform": "\"macOS\"", "Origin": "https://sneakerboxtlv.com",
                     "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty",
                     "Referer": "https://sneakerboxtlv.com/product-category/footwear/",
                     "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9"}
    offset = 0
    for i in range(12):
        product_urls = []

        product_data_file = json.load(open("product_data.json", "r"))
        for product in product_data_file["sneakerboxtlv"]:
            product_urls.append(product["product_url"])

        data = {"action": "more_prods", "offset": f"{offset}", "productCat": "footwear", "brand": '', "gender": ''}
        content = requests.post(url, headers=headers, cookies=cookies, data=data).content
        soup = BeautifulSoup(content, 'html.parser')

        product_parents = soup.find_all('div')
        for product_children in product_parents:
            if "product" in product_children.get('class'):
                product_name = product_children.find('a').find('div', class_='title').text.strip().replace("                                                ", " ")
                product_url = product_children.find('a').get("href")
                product_price = product_children.find('a').find('div', class_='price').text.strip()
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
                            "product_sizes": scrape_product_sizes(product_soup),
                            "product_image": scrape_product_image(product_soup)
                        }

                        # send product data to webhook
                        if product_data["product_url"] not in product_urls:
                            product_urls.append(product_data["product_url"])
                            new_shoe_message("Sneakerbox tlv", product_data["product_name"],
                                             product_data["product_url"],
                                             product_data["product_price"], "In Stock", product_data["product_sizes"],
                                             product_data["product_image"])
                            update_products_json_file("sneakerboxtlv", product_data)

        offset += 24


def update_products_json_file(company_name: str, product_data: dict):
    with open("product_data.json", 'r+') as file:
        file_data = json.load(file)
        file_data[company_name].append(product_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)
