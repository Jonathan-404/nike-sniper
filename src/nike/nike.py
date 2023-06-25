from src.nike import nike_scrape_functions

import requests
from bs4 import BeautifulSoup
import concurrent.futures
from src.Shoe import Shoe
from src.utils import *

ANCHOR_OFFSET = 24


def process_api_product_info(product):
    full_url = "https://www.nike.com/il" + product['url'][13:]
    product_price = product["price"]["currentPrice"]
    product_name = product["title"]
    product_image = product["images"]["portraitURL"]
    product_sizes = nike_scrape_functions.scrape_sizes(full_url)


    if not product_sizes:
        return None

    return Shoe("nike", product_name, full_url, product_price, product_image, product_sizes)


def get(url: str, keywords: list):
    urls = get_urls("nike")

    index = 0
    anchor = 0
    for keyword in keywords:
        first_response = requests.get(f'https://www.nike.com/il/w?q=dunk&vst={keyword}').content

        parse_response = str(first_response).split('"')
        for element in parse_response:
            if element == "totalResources":
                total_products = int(parse_response[index + 1][1:-1])
            index += 1

        api_url = f'https://api.nike.com/cic/browse/v2?queryid=products&anonymousId=3B92F143E7E35F9BC32752892407F7BF&country=il&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(IL)%26filter%3Dlanguage(en-GB)%26filter%3DemployeePrice(true)%26searchTerms%3D{keyword}%26anchor%3D{anchor}%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D24&language=en-GB&localizedRangeStr=%7BlowestPrice%7D%E2%80%94%7BhighestPrice%7D'
        while anchor < total_products:
            response = requests.get(api_url)
            api_data = response.json()

            products = api_data["data"]["products"]["products"]

            for product in products:
                shoe = process_api_product_info(product)
                if shoe and shoe.sizes:
                    if shoe.url not in urls:
                        shoe.discord_message()
                        shoe.update()
                        urls.append(shoe.url)

            anchor += ANCHOR_OFFSET
            api_url = f'https://api.nike.com/cic/browse/v2?queryid=products&anonymousId=3B92F143E7E35F9BC32752892407F7BF&country=il&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(IL)%26filter%3Dlanguage(en-GB)%26filter%3DemployeePrice(true)%26searchTerms%3D{keyword}%26anchor%3D{anchor}%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D24&language=en-GB&localizedRangeStr=%7BlowestPrice%7D%E2%80%94%7BhighestPrice%7D'

