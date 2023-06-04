import requests
from bs4 import BeautifulSoup
import concurrent.futures

ANCHOR_OFFSET = 24

anchor = ANCHOR_OFFSET


url = "https://www.nike.com/il/w/mens-shoes-nik1zy7ok"
api_url = f"https://api.nike.com/cic/browse/v2?queryid=products&anonymousId=CFD2FD8E39261E9F8455D413E1597666&country=il&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(IL)%26filter%3Dlanguage(en-GB)%26filter%3DemployeePrice(true)%26filter%3DattributeIds(16633190-45e5-4830-a068-232ac7aea82c%2C0f64ecc7-d624-4e91-b171-b83a03dd8550)%26anchor%3D{anchor}%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D24&language=en-GB&localizedRangeStr=%7BlowestPrice%7D%E2%80%94%7BhighestPrice%7D"



def scrape_first_products(products_urls, products_names, products_prices, products_images):

    response_content = requests.get(url).content
    soup = BeautifulSoup(response_content, 'html.parser')
    products_divs = soup.find_all('div', class_='product-card__body')

    for product_div in products_divs:

        link_elem = product_div.find('a', class_='product-card__link-overlay')
        link = link_elem['href'] if link_elem else None

        name_elem = product_div.find('div', class_='product-card__title')
        name = name_elem.text.strip() if name_elem else None

        price_elem = product_div.find('div', class_='product-price il__styling is--current-price css-11s12ax')
        price = price_elem.text.strip() if price_elem else None

        if link and name and price:
            price = price.replace('₪', '')

            products_urls.append(link)
            products_names.append(name)
            products_prices.append(price)

    for product_url in products_urls:
        product_response = requests.get(product_url).content
        soup = BeautifulSoup(product_response, 'html.parser')
        product_image = soup.find('img', class_='css-viwop1 u-full-width u-full-height css-m5dkrx')['src']
        if product_image:
            products_images.append(product_image)






def create_scroll_pages_list(api_url, pages_list):

    anchor = 0
    index = 0
    first_response = requests.get(url).content
    parse_response = str(first_response).split('"')

    for element in parse_response:
        if element == "totalResources":
            total_products = int(parse_response[index + 1][1:-1])
        index += 1


    for i in range((total_products // ANCHOR_OFFSET) + 1):
        response = requests.get(api_url)
        api_data = response.json()
        pages_list.append(api_data)
        anchor += ANCHOR_OFFSET
        api_url = f"https://api.nike.com/cic/browse/v2?queryid=products&anonymousId=CFD2FD8E39261E9F8455D413E1597666&country=il&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(IL)%26filter%3Dlanguage(en-GB)%26filter%3DemployeePrice(true)%26filter%3DattributeIds(16633190-45e5-4830-a068-232ac7aea82c%2C0f64ecc7-d624-4e91-b171-b83a03dd8550)%26anchor%3D{anchor}%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D24&language=en-GB&localizedRangeStr=%7BlowestPrice%7D%E2%80%94%7BhighestPrice%7D"



def scrape_api_products_details(pages_list, products_urls, products_names, products_prices, products_images):
    for page in pages_list:

        for product in page["data"]["products"]["products"]:

            full_url = "https://www.nike.com/il" + product['url'][13:]

            product_price = product["price"]["currentPrice"]
            product_name = product["title"]
            product_image = product["images"]["portraitURL"]

            products_urls.append(full_url)
            products_prices.append(product_price)
            products_names.append(product_name)
            products_images.append(product_image)



def scrape_sizes(products_urls, products_sizes):
    index = 1

    def process_product(product_url):
        product_sizes = []
        product_response = requests.get(product_url).content
        product_response = str(product_response).split('"')

        for i in range(len(product_response)):
            if product_response[i] == "localizedSize":
                current_size = product_response[i + 2]
                product_sizes.append(current_size)

        product_sizes = list(set(product_sizes))
        product_sizes = sorted(product_sizes, key=lambda x: float(x))
        return product_sizes

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(process_product, products_urls)

        for product_sizes in results:
            products_sizes.append(product_sizes)
            print(f"Finished product {index} sizes")
            index += 1



