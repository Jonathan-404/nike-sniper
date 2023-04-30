from keys import discord_webook
from bs4 import BeautifulSoup
import requests
import time


urls = ['https://www.jdsports.co.il/collections/nike-men-shoes-sneakers']
keywords = ['Dunk']


def main():
    check_keywords(urls)


def check_keywords(urls: list):

    links = []
    for url in urls:
        response = requests.get(url)
        content = response.content

        soup = BeautifulSoup(content, 'html.parser')
        product_items = soup.find_all('div', class_='product-item-meta')
        for product_item in product_items:
            h2 = product_item.find('h2', class_='product-item-meta__title')
            if h2 is not None:
                title = h2.text.strip()
                for keyword in keywords:
                    if keyword in title:
                        url_paramater = h2.get('href')
                        links.append(f"{url}{url_paramater}")
                        break
        print(links)


def webhook_send(discord_webhook: str, message: str):
    pass



if __name__ == '__main__':
    main()