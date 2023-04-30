from keys import discord_webhook
from discordwebhook import Discord
from bs4 import BeautifulSoup
import requests
import time

urls = ['https://www.jdsports.co.il/collections/nike-men-shoes-sneakers']
keywords = ['Dunk']


def main():
    print(check_price('https://www.jdsports.co.il/products/jodq0560160'))


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


def check_price(url: str):
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')

    price = soup.find('span', class_='price price--large')

    return ''.join(filter(lambda x: x.isdigit() or x == '.', price.text))


def webhook_send(discord_webhook: str, message: str):
    webhook = Discord(url=discord_webhook)

    webhook.post(
        embeds=[
            {
                "author": {
                    "name": "Shoes Website",
                    "url": "https://shoes.com/",
                    "icon_url": "https://shoes.com/",
                },
                "title": "NEW SHOE!",
                "description": "New shoe has been released on the website!",
                "fields": [
                    {"name": "Price", "value": "999.0 ILS", "inline": True},
                    {"name": "Status", "value": "In Stock", "inline": True},
                    {"name": "Available Sizes", "value": "99, 99, 99", "inline": False},
                ],
                "thumbnail": {"url": "https://picsum.photos/80/60"},
                "image": {"url": "https://picsum.photos/400/300"},
                "footer": {
                    "text": "Embed Footer",
                    "icon_url": "Rights Reserved to Jonathan & Liam",
                },
            }
        ],
    )


if __name__ == "__main__":
    main()
