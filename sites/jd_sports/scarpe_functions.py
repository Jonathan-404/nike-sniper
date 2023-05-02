from bs4 import BeautifulSoup
import requests
import json


def scrape_product_price(url: str):
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')
    if soup.find('span', class_='price price--large'):
        return ''.join(filter(lambda x: x.isdigit() or x == '.', soup.find('span', class_='price price--large').text))
    elif soup.find('span', class_='price price--highlight price--large'):
        return ''.join(filter(lambda x: x.isdigit() or x == '.', soup.find('span', class_='price price--highlight price--large').text))


def scrape_product_image(url: str):
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')
    return soup.find('div', class_='product__media-image-wrapper').find('img').get('src')[2:]


def scrape_product_sizes(url: str):
    sizes = []

    content = requests.get(url, timeout=2).content
    soup = BeautifulSoup(content, 'html.parser')

    for size in json.loads(soup.find('script', type='application/ld+json').text)['offers']:
        if size['availability'] == 'https://schema.org/InStock':
            sizes.append(size['name'].split(' / ')[0])

    return sizes
