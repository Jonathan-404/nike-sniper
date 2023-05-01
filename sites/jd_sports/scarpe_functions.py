from bs4 import BeautifulSoup
import requests


def scrape_product_price(url: str):
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')
    return ''.join(filter(lambda x: x.isdigit() or x == '.', soup.find('span', class_='price price--large').text))


def scrape_product_image(url: str):
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')
    return soup.find('div', class_='product__media-image-wrapper').find('img').get('src')[2:]


def scrape_product_sizes(url: str):
    sizes = []
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')
    sizes_parent = soup.find('div', class_='block-swatch-list').find_all('div', class_='block-swatch')

    for size_children in sizes_parent:
        sizes.append(size_children.find('label', class_='block-swatch__item').text.strip())
    return sizes
