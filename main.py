from keys import discord_webhook, urls, keywords
from discordwebhook import Discord
from bs4 import BeautifulSoup
import requests
import time

# sites algorithms are imported from sites directory

from sites import jd_sports
print(jd_sports.x)


def main():
    check_keywords(urls, keywords)


def check_keywords(urls: list, keywords: list):
    links = []

    old_links_file = open("old_links.txt", "r")
    old_links = old_links_file.read().split('\n')
    old_links_file.close()

    for url in urls:
        content = requests.get(url).content

        soup = BeautifulSoup(content, 'html.parser')
        product_items = soup.find_all('div', class_='product-item-meta')

        for product_item in product_items:
            h2 = product_item.find('h2', class_='product-item-meta__title')

            product_name = h2.text.strip()

            for keyword in keywords:
                if keyword in product_name:

                    url_paramater = h2.get('href')
                    link = f"https://www.jdsports.co.il{url_paramater}"

                    if link not in old_links:
                        old_links.append(link)

                    break

    old_links_file = open("old_links.txt", "w")
    for link in old_links:
        old_links_file.write(link + "\n")
    old_links_file.close()


def check_price(url: str):
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')

    price = soup.find('span', class_='price price--large')
    return ''.join(filter(lambda x: x.isdigit() or x == '.', price.text))


# webhook_send(discord_webhook, "JD Sports", title, link, check_price(link), "In Stock", [], "")
def webhook_send(discord_webhook: str, website_name: str, product_name: str, product_link: str, product_price: str, product_status: str, product_sizes: list, product_image: str):
    discord = Discord(url=discord_webhook)

    discord.post(
        embeds=[
            {
                "author": {
                    "name": website_name,
                    "url": product_link,
                    "icon_url": "https://picsum.photos/24/24",
                },
                "title": "New Shoe Listed!",
                "description": f"New shoe has been listed on {website_name}",
                "fields": [
                    {"name": "Product Name", "value": product_name, "inline": True},
                    {"name": "Price", "value": product_price, "inline": True},
                    {"name": "Status", "value": product_status},
                ],
                "thumbnail": {"url": product_image},
                "footer": {
                    "text": "Embed Footer",
                    "icon_url": "https://picsum.photos/20/20",
                },
            }
        ],
    )


if __name__ == "__main__":
    main()
