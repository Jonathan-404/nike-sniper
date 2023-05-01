from bs4 import BeautifulSoup
import requests


def scrape_product_price(url: str):
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')
    print(''.join(filter(lambda x: x.isdigit() or x == '.', soup.find('span', class_='price price--large').text)))

    return ''.join(filter(lambda x: x.isdigit() or x == '.', soup.find('span', class_='price price--large').text))


def scrape_product_image(url: str):
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')
    print(soup.find('div', class_='product__media-image-wrapper').find('img').get('src')[2:])
    return soup.find('div', class_='product__media-image-wrapper').find('img').get('src')[2:]

