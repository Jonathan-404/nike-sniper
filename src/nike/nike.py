from src.nike import nike_scrape_functions

import requests
from bs4 import BeautifulSoup
import concurrent.futures
from src.Shoe import Shoe
from src.utils import *

ANCHOR_OFFSET = 24
NOT_EXIST = -1




def process_first_products(product_div):
    link_elem = product_div.find('a', class_='product-card__link-overlay')
    link = link_elem['href'] if link_elem else None

    name_elem = product_div.find('div', class_='product-card__title')
    name = name_elem.text.strip() if name_elem else None

    price_elem = product_div.find('div', class_='product-price il__styling is--current-price css-11s12ax')
    price = price_elem.text.strip() if price_elem else None

    if link and name and price:
        price = price.replace('₪', '')

        product_response = requests.get(link).content
        soup = BeautifulSoup(product_response, 'html.parser')

        product_image = soup.find('img', class_='css-viwop1 u-full-width u-full-height css-m5dkrx')['src'] if soup.find('img', class_='css-viwop1 u-full-width u-full-height css-m5dkrx') else None


        if not product_image:
            div_tag = soup.find('div', class_='css-b8rwz8 tooltip-component-container')
            img_tag = div_tag.find('img')
            product_image = img_tag['src']


        sizes = nike_scrape_functions.scrape_sizes(link)
        return Shoe("nike", name, link, price, product_image, sizes)
    else:
        return None



def get_first(url: str, keywords: list):
    response_content = requests.get(url).content
    soup = BeautifulSoup(response_content, 'html.parser')
    products_divs = soup.find_all('div', class_='product-card__body')
    urls = get_urls("nike")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_first_products, product_div) for product_div in products_divs]

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                shoe = result

                for keyword in keywords:
                    if keyword in shoe.name:
                        if shoe.url not in urls:
                            shoe.discord_message()
                            shoe.update()
                            urls.append(shoe.url)
                if shoe.url in urls:
                    check_for_updates(shoe.sizes, get_stored_sizes(shoe.site, shoe.url), shoe)






def process_api_product_info(product):
    full_url = "https://www.nike.com/il" + product['url'][13:]
    product_price = product["price"]["currentPrice"]
    product_name = product["title"]
    product_image = product["images"]["portraitURL"]
    product_sizes = nike_scrape_functions.scrape_sizes(full_url)


    if not product_sizes:
        return None

    return Shoe("nike", product_name, full_url, product_price, product_image, product_sizes)


def get_api(url: str, keywords: list):
    anchor = 24
    api_url = f"https://api.nike.com/cic/browse/v2?queryid=products&anonymousId=CFD2FD8E39261E9F8455D413E1597666&country=il&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(IL)%26filter%3Dlanguage(en-GB)%26filter%3DemployeePrice(true)%26filter%3DattributeIds(16633190-45e5-4830-a068-232ac7aea82c%2C0f64ecc7-d624-4e91-b171-b83a03dd8550)%26anchor%3D{anchor}%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D24&language=en-GB&localizedRangeStr=%7BlowestPrice%7D%E2%80%94%7BhighestPrice%7D"
    index = 0
    urls = get_urls("nike")

    first_response = requests.get(api_url).content
    parse_response = str(first_response).split('"')

    for element in parse_response:
        if element == "totalResources":
            total_products = int(parse_response[index + 1][1:-1])
        index += 1

    with concurrent.futures.ThreadPoolExecutor() as executor:
        while anchor < total_products:
            response = requests.get(api_url)
            api_data = response.json()

            products = api_data["data"]["products"]["products"]
            futures = [executor.submit(process_api_product_info, product) for product in products]

            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    shoe = result
                    for keyword in keywords:
                        if keyword in shoe.name:
                            if shoe.url not in urls:
                                shoe.discord_message()
                                shoe.update()
                                urls.append(shoe.url)
                    if shoe.url in urls:
                        check_for_updates(shoe.sizes, get_stored_sizes(shoe.site, shoe.url), shoe)

            anchor += ANCHOR_OFFSET
            api_url = f"https://api.nike.com/cic/browse/v2?queryid=products&anonymousId=CFD2FD8E39261E9F8455D413E1597666&country=il&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(IL)%26filter%3Dlanguage(en-GB)%26filter%3DemployeePrice(true)%26filter%3DattributeIds(16633190-45e5-4830-a068-232ac7aea82c%2C0f64ecc7-d624-4e91-b171-b83a03dd8550)%26anchor%3D{anchor}%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D24&language=en-GB&localizedRangeStr=%7BlowestPrice%7D%E2%80%94%7BhighestPrice%7D"




def main():


    pass



if __name__ == "__main__":
    main()